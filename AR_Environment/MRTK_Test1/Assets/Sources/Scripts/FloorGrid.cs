using Microsoft.MixedReality.Toolkit.SpatialAwareness;
using Microsoft.MixedReality.Toolkit.Experimental.SpatialAwareness;

using System;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Assertions;
using Random = UnityEngine.Random;

namespace ParkourApp
{
    /** <summary>Class <c>FloorGrid<c> is a descrete grid representation of multiple 
    Scene Understanding floors. The grid is x-y-axis aligned with a principal floor and
    provides a 3D to 2D transformation. 
    **/
    public class FloorGrid : MonoBehaviour
    {

        // logic with public acessors
        public bool IsInitiallized => _IsInitiallized;
        private bool _IsInitiallized = false;

        public bool IsRasterized => _IsRasterized;
        private bool _IsRasterized = false;

        public bool IsDistances => _IsDistances;
        private bool _IsDistances = false;


        #region Private Fields

        // private attribute for 2D-3D transform;
        private Bounds gridBounds;
        private Vector3 grid_origin_local;
        private Vector3 grid_origin_world;
        private Vector3 x_step_world;
        private Vector3 y_step_world;


        // private attributes for discrete grid representation
        private Vector2Int size;
        private int[,] walkableGrid = null;
        private float[,] distanceGrid = null;


        // private attributes for grid visualization
        private float max_dist;
        private float min_dist;
        private int n_reachable;
        private GameObject gridCanvas;

        #region Serialized Fields

        [SerializeField]
        private float resolution = 0.1f;

        [SerializeField]
        private float heightThreshold = 1.8f;

        [SerializeField]
        private float aboveFloorEpsilon = 0.05f;

        [SerializeField]
        private float pathSmootheness = 1.0f;

        [SerializeField]
        // Dangerous: if larger than distance from obstacle to entry point
        private float pathMinBorderDistance = 0.00f; // in meters

        #endregion Serialized Fields

        private Vector2Int startCellBackup = new Vector2Int(-1, -1); // cell indexes are >=0

        // define const 8-neighborhood
        private static readonly Vector2Int[] neighborhood = new Vector2Int[] {
                new Vector2Int(-1,-1),
                new Vector2Int(-1,+0),
                new Vector2Int(-1,+1),
                new Vector2Int(+0,-1),
                // new Vector2Int(+0,+0);
                new Vector2Int(+0,+1),
                new Vector2Int(+1,-1),
                new Vector2Int(+1,+0),
                new Vector2Int(+1,+1),
                };

        #endregion Private Fields

        /** Defines the transform of the floor grid according to the primary floor
        and determines the extents of the grid to include all other floors. 
        Sets attributes:
        - transform.rotation, transform.position, gridBounds, size
        - grid_origin_local, grid_origin_world, x_step_world, y_step_world
        **/
        public void InitiallizeFloors(List<SpatialAwarenessSceneObject> floors)
        {
            if (floors.Count == 0)
                return;

            // set rotation and position of floor grid according to primary floor
            transform.rotation = floors[0].Rotation;
            transform.position = floors[0].Position;

            // get axis aligned bounds in local coordinates from MeshFilter
            gridBounds = floors[0].GameObject.GetComponentInChildren<MeshFilter>().mesh.bounds;

            // extend bounds with extents of other floors in local cooridnate system
            foreach (var floor in floors.GetRange(1, floors.Count - 1))
            {
                Vector3 cube = floor.GameObject.GetComponentInChildren<MeshFilter>().mesh.bounds.extents;
                Transform fTransform = floor.GameObject.transform;

                List<Vector3> corners = new List<Vector3>();
                corners.Add(new Vector3(+cube.x, +cube.y, +cube.z));
                corners.Add(new Vector3(+cube.x, +cube.y, -cube.z));
                corners.Add(new Vector3(+cube.x, -cube.y, +cube.z));
                corners.Add(new Vector3(+cube.x, -cube.y, -cube.z));
                corners.Add(new Vector3(-cube.x, +cube.y, +cube.z));
                corners.Add(new Vector3(-cube.x, +cube.y, -cube.z));
                corners.Add(new Vector3(-cube.x, -cube.y, +cube.z));
                corners.Add(new Vector3(-cube.x, -cube.y, -cube.z));

                foreach (Vector3 corner in corners)
                {
                    gridBounds.Encapsulate(transform.InverseTransformPoint(fTransform.TransformPoint(corner)));
                }
            }

            /* To Debug Algos: manually defined toy-grid of size 9x9
            Vector3 small = Vector3.one * 4 * resolution;
            small.z = gridBounds.extents.z;
            gridBounds.extents = small;
            */

            // Round grid bounds up to a multiple of the resolution
            size.x = ((int)((gridBounds.max.x - gridBounds.min.x) / resolution)) + 1;
            size.y = ((int)((gridBounds.max.y - gridBounds.min.y) / resolution)) + 1;
            gridBounds.Encapsulate(new Vector3(
                gridBounds.min.x + resolution * size.x,
                gridBounds.min.y + resolution * size.y,
                gridBounds.max.z));

            // Construct grids
            walkableGrid = new int[size.x, size.y];
            distanceGrid = new float[size.x, size.y];

            // define grid 2D-3D transform
            grid_origin_local = gridBounds.min;
            grid_origin_local.x += resolution / 2.0f;
            grid_origin_local.y += resolution / 2.0f;

            grid_origin_world = transform.TransformPoint(grid_origin_local);
            x_step_world = transform.TransformVector(resolution * Vector3.right);
            y_step_world = transform.TransformVector(resolution * Vector3.up);

            Debug.Log("Initialized Grid:"
                + "\n - has bounds " + gridBounds
                + "\n - " + size.x + "x" + size.y + " cells "
                + "\n - " + size.x * size.y * sizeof(int) / 1e3 + " MB");

            // logic to avoid illposed states
            _IsInitiallized = true;
            _IsRasterized = false;  // requires (re-)rasteriation
            _IsDistances = false;   // requires (re-)calculation of distances
        }

        public Vector3 TransformPoint(int x, int y)
        {
            return TransformPoint(new Vector2Int(x, y));
        }

        public Vector3 TransformPoint(Vector2Int cell)
        {
            return grid_origin_world + x_step_world * cell.x + y_step_world * cell.y;
        }

        public Quaternion TransformAngle(float angle_deg)
        {
            Vector2 dir_local = rotate(new Vector2(1, 0), angle_deg);
            Vector3 dir_world = transform.TransformDirection(new Vector3(dir_local.x, dir_local.y, 0));
            return Quaternion.FromToRotation(new Vector3(1, 0, 0), dir_world);
            //return Quaternion.Euler(0, transform.rotation.eulerAngles.y + angle_deg, 0);
            //return transform.rotation * Quaternion.Euler(0, angle_deg, 0);
        }

        public Vector2Int InverseTransformPoint(Vector3 position)
        {
            position = transform.InverseTransformPoint(position);
            position = (position - grid_origin_local) / resolution;
            return Vector2Int.RoundToInt((Vector2)position);
        }

        /** Rasterizes the Spatial Awareness Layer into a discrete grid.
        Sets attributes:
        - walkableGrid
        **/
        public void Rasterize()
        {
            if (!_IsInitiallized)
            {
                Debug.LogError("FloorGrid.Rasterize(): abort because is not initiallized");
                return;
            }

            // Prepare raycasting in global coordinates, locally, up is -z
            Vector3 ray_origin = grid_origin_local;
            ray_origin.z -= heightThreshold;
            ray_origin = transform.TransformPoint(ray_origin);

            Vector3 ray_direction = transform.TransformVector(new Vector3(0, 0, 1));
            int mask = LayerMask.GetMask("Spatial Awareness");
            float max_distance = heightThreshold + 0.1f;

            // Rasterize orthogonal projection of walkable area onto the floor
            RaycastHit hit;
            int hit_counter = 0;

            System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
            sw.Start();
            for (int i = 0; i < size.x; i++)
            {
                for (int j = 0; j < size.y; j++)
                {

                    if (walkableGrid[i, j] <= 0) // no object placed there
                        walkableGrid[i, j] = -1; // default case: not walkable

                    // overwrite not walkable or object cells with walkable if ray hits floor
                    float temp_max_distance = max_distance;
                    Vector3 temp_ray_origin = ray_origin;
                    while (Physics.Raycast(temp_ray_origin, ray_direction, out hit, temp_max_distance, mask))
                    {
                        // check whether object is floor
                        Transform parent = hit.collider.transform.parent;
                        if (parent != null && parent.name.Contains("Floor"))
                        {
                            hit_counter++;
                            walkableGrid[i, j] = 0; // is walkable
                            break;
                        }

                        // forward ray if hitpoint is on world mesh and close to floor
                        if (parent != null && parent.name.Contains("World")
                            && gridBounds.min.z - transform.InverseTransformPoint(hit.point).z < aboveFloorEpsilon)
                        {
                            temp_max_distance = max_distance - hit.distance;      // reduce ray length
                            temp_ray_origin = hit.point + ray_direction * 1e-5f; // avoid self-intersection
                        }
                        else // don't forward ray, not walkable
                            break;
                    }
                    ray_origin += y_step_world; // prepare next sample
                }

                // prepare next 
                ray_origin += x_step_world;
                ray_origin -= size.y * y_step_world;
            }

            sw.Stop();
            Debug.Log("Rasterized Grid:"
                + "\n - total cells: " + size.x * size.y
                + "\n - total hits: " + hit_counter
                + "\n - took " + sw.ElapsedMilliseconds + "ms");

            // logic to avoid illposed states
            _IsRasterized = true;
            _IsDistances = false;   // requires (re-)calculation of distances
        }

        /** Adds a rectangle specified by extents and ID at cell with rotation angle to the grid.
        Updates attributes: walkableGrid
        **/
        public void AddRectangle(int rectangleID, Vector2 rect, Vector2Int cell, float angle)
        {
            if (!_IsInitiallized)
            {
                Debug.LogError("FloorGrid.AddRectangle(): abort because is not intitiallized");
                return;
            }

            Assert.IsTrue(rectangleID >= 0, "rectangleID needs to greater or equal to zero");
            int grid_rectangleID = rectangleID + 1; // grid obects are 1-indexed

            // compute number of steps
            float stepsize = resolution / 2;
            Vector2Int n_steps = Vector2Int.RoundToInt(2 * rect / stepsize + Vector2.one);

            // local object to floor transform and [m] to grid units
            Vector2 rect_rot = rotate(rect, angle) / resolution;
            Vector2 right_rot = rotate(Vector2.right, angle) / resolution;
            Vector2 up_rot = rotate(Vector2.up, angle) / resolution;

            // start with outer corner of objects and iterate n_steps with stepsize
            int sample_counter = 0;
            Vector2Int index;
            Vector2 sample = cell - rect_rot; // start with lower left corner
            for (float i = 0; i < n_steps.x; i++)
            {
                for (int j = 0; j < n_steps.y; j++)
                {
                    index = Vector2Int.RoundToInt(sample);
                    sample += up_rot * stepsize;
                    if (index.x < 0 || size.x <= index.x    // x out of bounds
                        || index.y < 0 || size.y <= index.y   // y out of bounds
                        || walkableGrid[index.x, index.y] == -1)  // already occupied by scene 
                        continue;

                    sample_counter++;
                    walkableGrid[index.x, index.y] = grid_rectangleID;
                }
                sample += right_rot * stepsize;
                sample -= n_steps.y * up_rot * stepsize;
            }
            //Debug.Log("Samplecounter: " + sample_counter);

            // logic to avoid illposed states
            _IsDistances = false; // requires (re-)calculation of distances
        }

        /** Removes an object specified by ID from the grid.
        Updates attributes: walkableGrid
        **/
        public void RemoveObject(int objectID)
        {
            Assert.IsTrue(objectID >= 0, "objectID needs to greater or equal to zero");
            float grid_objectID = objectID + 1; // grid objects are 1-indexed
            for (int x = 0; x < size.x; x++)
            {
                for (int y = 0; y < size.y; y++)
                {
                    if (walkableGrid[x, y] == grid_objectID)
                    {
                        walkableGrid[x, y] = 0;
                    }
                }
            }

            // logic to avoid illposed states
            _IsDistances = false; // requires (re-)calculation of distances
        }

        /** Determines all reachable grid tiles from bfsRoot and calculates 
        the distance to the closest non-walkable tile.
        Sets attributes:
        - distanceGrid
        - max_dist, min_dist, n_reachable
        **/
        public void CalculateDistances(Vector3 startPosition)
        {
            CalculateDistances(InverseTransformPoint(startPosition));
        }

        public void CalculateDistances(Vector2Int startCell)
        {
            if (!_IsRasterized)
            {
                Debug.LogError("FloorGrid.calculateDistances(): abort because is not rasterized");
                return;
            }

            // if start cell is not walkable
            if (startCell.x < 0 || size.x <= startCell.x    // x out of bounds
                || startCell.y < 0 || size.y <= startCell.y // y out of bounds
                || walkableGrid[startCell.x, startCell.y] != 0) // is not walkable
            {

                if (startCellBackup == new Vector2Int(-1, -1))  // if no backup is available
                {
                    Debug.LogError("FloorGrid.calculateDistances(): abort because startCell is not walkable.");
                    return;
                }

                // recover startcell from backup
                startCell = startCellBackup;
                Debug.LogWarning("FloorGrid.calculateDistances(): continue with backup but startCell is not walkable.");
            }

            // store current startCell as backup
            startCellBackup = startCell;

            // datastructures for two BFS passes          
            Queue<Vector2Int> reachable_queue = new Queue<Vector2Int>();
            Queue<Vector2Int> distance_queue = new Queue<Vector2Int>();

            System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
            n_reachable = 0;
            sw.Start();

            // set all distances to zero
            Array.Clear(distanceGrid, 0, distanceGrid.Length);

            // initiallize with 
            reachable_queue.Enqueue(startCell);
            distanceGrid[startCell.x, startCell.y] = float.PositiveInfinity; // set visited

            // expanding BFS forward pass
            Vector2Int cell, neigh;
            while (reachable_queue.Count > 0)
            {
                cell = reachable_queue.Dequeue(); // current cell
                n_reachable++;

                // enqueue walkable neighbors
                foreach (Vector2Int step in neighborhood)
                {
                    neigh = cell + step; // neighbor

                    // if cell has a non-walkable neighbor
                    if (neigh.x < 0 || size.x <= neigh.x    // x out of bounds
                        || neigh.y < 0 || size.y <= neigh.y // y out of bounds
                        || walkableGrid[neigh.x, neigh.y] != 0) // is not walkable
                    {
                        // add cell to start of second BFS pass and set init distance
                        float cell_dist = distanceGrid[cell.x, cell.y];
                        float step_dist = step.magnitude * resolution;

                        // only add if not already in queue 
                        if (!distance_queue.Contains(cell))
                            distance_queue.Enqueue(cell);

                        // set to smallest step over all neighbors
                        distanceGrid[cell.x, cell.y] = Mathf.Min(cell_dist, step_dist);
                        continue;
                    }

                    if (distanceGrid[neigh.x, neigh.y] > 0) // neighbor already visited
                        continue;

                    reachable_queue.Enqueue(neigh); // visit neighbor
                    distanceGrid[neigh.x, neigh.y] = float.PositiveInfinity; // set visited
                }

                /* To debug the behaviour of this algo in the Unity Console
                Debug.Log("cell: " + cell 
                    + "\nqueue: " + queue2str<Vector2Int>(distance_queue)
                    + "\ngrid:\n" + distGrid2str(distanceGrid, cell));
                */
            }


            // gathering BFS pass
            max_dist = 1;
            while (distance_queue.Count > 0)
            {
                cell = distance_queue.Dequeue(); // current cell
                max_dist = Mathf.Max(max_dist, distanceGrid[cell.x, cell.y]);
                // visit_counter++;

                // enqueue walkable neighbors
                foreach (Vector2Int step in neighborhood)
                {
                    neigh = cell + step;     // neighbor

                    // if cell has a non-walkable neighbor
                    if (neigh.x < 0 || size.x <= neigh.x    // x out of bounds
                        || neigh.y < 0 || size.y <= neigh.y // y out of bounds
                        || walkableGrid[neigh.x, neigh.y] != 0) // is not walkable
                    {
                        continue;
                    }

                    // add cell to start of second BFS pass and set init distance
                    float cell_dist = distanceGrid[cell.x, cell.y];
                    float neigh_dist = distanceGrid[neigh.x, neigh.y];
                    float step_dist = step.magnitude * resolution;
                    bool first_visited = (neigh_dist == float.PositiveInfinity);

                    if (cell_dist + step_dist >= neigh_dist)
                        continue;

                    // found new shortest distance => need to put it into queue
                    if (first_visited || !distance_queue.Contains(neigh))
                        distance_queue.Enqueue(neigh);

                    distanceGrid[neigh.x, neigh.y] = cell_dist + step_dist;

                    /* Standard BFS, but not correct :
                    if (neigh_dist < float.PositiveInfinity) // neighbor already visited
                        continue;
                    distance_queue.Enqueue(neigh); // visit neighbor
                    grid[neigh.x, neigh.y] = cell_dist + step_dist; // set visited
                    */
                }
            }
            sw.Stop();
            Debug.Log("Calculated Distances:"
                + "\n - largest distance: " + max_dist
                + "\n - reachable cells: " + n_reachable
                + "\n - " + size.x * size.y * sizeof(float) / 1e3 + " MB"
                + "\n - took " + sw.ElapsedMilliseconds + "ms");

            // statistics for drawing
            min_dist = resolution;

            // logic to avoid illposed states
            _IsDistances = true;
        }


        /** Calculate possible placements of reactangle rect at specified angles.
        Sets attributes: none.
        **/
        public List<(Vector2Int, float)> CalculatePlacements(Vector2 rect, float[] angles, int max_placements)
        {
            if (!IsDistances)
                Debug.LogWarning("FloorGrid.calculatePlacements(): continue but distances are not up-to-date");

            // in world coordinates, y-axis is 'up'
            float outerRadius = rect.magnitude;
            float innerradius = Mathf.Sqrt(2 * Mathf.Pow(Mathf.Min(rect.x, rect.y), 2));

            if (max_placements <= 0)
                max_placements = n_reachable;

            var placements = new List<(Vector2Int, float)>();
            for (int x = 0; x < size.x; x++)
            {
                for (int y = 0; y < size.y; y++)
                {

                    Vector2Int cell = new Vector2Int(x, y);
                    if (outerRadius < distanceGrid[x, y]) // is placeable for sure with arbitrary angle
                    {
                        float angle = angles[Random.Range(0, angles.Length)];
                        placements.Add((cell, angle));
                    }
                    else if (innerradius < distanceGrid[x, y]) // might be placeable with some specific angles
                    {
                        // iterate over angles in random order
                        foreach (float angle in angles.OrderBy(_ => Random.Range(0, 1)))
                        {
                            if (checkRectanglePlaceability(rect, cell, angle))
                            {   // found angle => add placement
                                placements.Add((cell, angle));
                                break;
                            }
                        }
                    }
                    // do not compute more placements than requested
                    if (max_placements <= placements.Count)
                        return placements;
                }
            }

            return placements;
        }


        /** Calculate path from start to end cell. 
        Sets attributes: none.
        **/
        public List<Vector2Int> CalculatePath(Vector2Int start, Vector2Int end)
        {
            if (!IsDistances)
                Debug.LogWarning("FloorGrid.CalculatePath(): continue but distances are not up-to-date");

            var path = new List<Vector2Int>();
            if (start == end)
                return path;

            // Convert indeces
            var distanceQueue = new Queue<Vector2Int>();
            float[,] distanceFromStart = new float[size.x, size.y];
            distanceQueue.Enqueue(start);

            // Use BFS since this can be faster to find correct direction than BFS (maybe?)
            Vector2Int cell, neigh;
            while (distanceQueue.Count > 0)
            {
                cell = distanceQueue.Dequeue(); // current cell
                foreach (Vector2Int step in neighborhood)
                {
                    neigh = cell + step;     // neighbor

                    // if cell has a non-walkable neighbor
                    if (neigh.x < 0 || size.x <= neigh.x    // x out of bounds
                        || neigh.y < 0 || size.y <= neigh.y // y out of bounds
                        || walkableGrid[neigh.x, neigh.y] != 0)     // is not walkable
                    {
                        continue;
                    }

                    float cell_dist = distanceFromStart[cell.x, cell.y];
                    float neigh_dist = distanceFromStart[neigh.x, neigh.y];
                    float step_dist = step.magnitude * resolution;
                    bool first_visited = (neigh_dist == 0);

                    /* penalize cells close to borders:
                     * A linear penalty would allow for shortcuts close to border, since path length 
                     * and distance border fight against each other and are of the same magnitude O(n).
                     * The square penalty will always win against shortest length, but come into play 
                     * if some paths are similarly optimal wrt. to boundary distance.
                     * This smoothness can be controlled by a parameter within the square. */
                    float penalty = Mathf.Pow(pathSmootheness * (max_dist - distanceGrid[neigh.x, neigh.y]), 2);
                    float new_dist = cell_dist + step_dist + penalty;

                    if (neigh == start)
                        continue;
                    if (new_dist - neigh_dist >= -0.00001 && neigh_dist != 0) // Already found a better path to this neighbour
                        continue;
                    if (distanceFromStart[end.x, end.y] != 0 // A path to end has been found
                        && distanceFromStart[end.x, end.y] <= Mathf.Min(new_dist, neigh_dist)) // neighbor is worse than already found path
                        continue;
                    if (distanceGrid[neigh.x, neigh.y] < pathMinBorderDistance) // Neighbor is too close to a wall
                        continue;

                    // found new shortest distance => need to put it into queue
                    if (!distanceQueue.Contains(neigh))
                        distanceQueue.Enqueue(neigh);
                    distanceFromStart[neigh.x, neigh.y] = new_dist;
                }
            }

            if (distanceFromStart[end.x, end.y] == 0)
            {
                Debug.Log("No path was found.");
                return path;
            }

            Debug.Log("Found path with cost: " + distanceFromStart[end.x, end.y]);

            // Now let's identify the path, trace backwards from end
            Boolean found_path = false;
            path.Add(end);
            cell = end;
            Vector2Int bestNeighbor;
            while (!found_path)
            {
                bestNeighbor = Vector2Int.down;
                foreach (Vector2Int step in neighborhood)
                {
                    neigh = cell + step;
                    if (neigh.x < 0 || size.x <= neigh.x    // x out of bounds
                        || neigh.y < 0 || size.y <= neigh.y) // y out of bounds
                        continue;
                    if (distanceFromStart[neigh.x, neigh.y] != 0 || neigh == start) // neighbor is valid candidate, or we found the start
                        if (bestNeighbor == Vector2Int.down || distanceFromStart[neigh.x, neigh.y] < distanceFromStart[bestNeighbor.x, bestNeighbor.y])
                            bestNeighbor = neigh;
                }
                cell = bestNeighbor;
                path.Add(cell);
                if (cell == start) found_path = true;
            }
            path.Reverse();
            return path;
        }

        /** Show Grid representation on a rectangular Canvas
        Sets attributes: gridCanvas
        **/
        public void ShowGrid()
        {
            if (!_IsInitiallized)
            {
                Debug.LogError("FloorGrid.ShowGrid(): abort because is not rasterized");
                return;
            }

            // Configure Grid Quad
            if (gridCanvas == null)
            {
                gridCanvas = GameObject.CreatePrimitive(PrimitiveType.Quad);
                gridCanvas.name = "GridCanvas";
            }
            Vector3 localpos = gridBounds.center;
            localpos.z = gridBounds.min.z;
            gridCanvas.transform.position = transform.TransformPoint(localpos);
            gridCanvas.transform.rotation = transform.rotation; // locally zero rotation
            gridCanvas.transform.localScale = 2.0f * gridBounds.extents;
            gridCanvas.transform.SetParent(transform);

            int n_channels = 4;
            byte[] bytearray = new byte[size.x * size.y * n_channels];

            const int colorIntensity = 60;
            for (int x = 0; x < size.x; x++)
            {
                for (int y = 0; y < size.y; y++)
                {
                    int index = n_channels * (y * size.x + x);

                    if (walkableGrid[x, y] < 0) // not-walkable red
                    {
                        bytearray[index + 0] = (byte)(colorIntensity); // red
                    }

                    if (walkableGrid[x, y] > 0) // objects orange
                    {
                        bytearray[index + 0] = (byte)(colorIntensity); // red
                        bytearray[index + 1] = (byte)(colorIntensity); // green
                    }

                    if (walkableGrid[x, y] == 0) // walkable area green
                    {
                        if (!IsDistances)
                        {
                            bytearray[index + 1] = (byte)(colorIntensity); // green
                        }
                        else
                        {   // linear scale green between 100 and 255:
                            float percentage = (distanceGrid[x, y] - min_dist) / (max_dist - min_dist);
                            bytearray[index + 1] = (byte)(100 + 155 * percentage);
                        }
                    }

                    // transparancy
                    bytearray[index + 3] = (byte)(80);
                }
            }

            // load texture onto grid quad
            Texture2D tex = new Texture2D(size.x, size.y, TextureFormat.RGBA32, false);
            tex.filterMode = FilterMode.Point;
            tex.LoadRawTextureData(bytearray);
            tex.Apply();

            gridCanvas.GetComponent<Renderer>().enabled = true;
            gridCanvas.GetComponent<Renderer>().material.SetTexture("_MainTex", tex);
            // Change rendering mode to transparent
            //gridCanvas.GetComponent<Renderer>().material.SetOverrideTag("RenderType", "Transparent");
            //gridCanvas.GetComponent<Renderer>().material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
            //gridCanvas.GetComponent<Renderer>().material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
            //gridCanvas.GetComponent<Renderer>().material.SetInt("_ZWrite", 0);
            //gridCanvas.GetComponent<Renderer>().material.DisableKeyword("_ALPHATEST_ON");
            //gridCanvas.GetComponent<Renderer>().material.EnableKeyword("_ALPHABLEND_ON");
            //gridCanvas.GetComponent<Renderer>().material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
            //gridCanvas.GetComponent<Renderer>().material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
        }

        public void HideGrid()
        {
            if (gridCanvas != null && gridCanvas.GetComponent<Renderer>() != null)
                gridCanvas.GetComponent<Renderer>().enabled = false;
        }

        /** Deletes the Grid
        Deletes attributes:
        - walkableGrid, distanceGrid, gridCanvas
        **/
        public void DeleteGrid()
        {
            walkableGrid = null;
            distanceGrid = null;
            Destroy(gridCanvas);

            _IsInitiallized = false;
            _IsRasterized = false;
            _IsDistances = false;
        }

        #region Private Helper Functions

        // Rotate clockwise by angle theta in degrees
        private Vector2 rotate(Vector2 vec, float theta_deg)
        {
            float cosTheta = Mathf.Cos(theta_deg * Mathf.PI / 180);
            float sinTheta = Mathf.Sin(theta_deg * Mathf.PI / 180);
            return new Vector2(cosTheta * vec.x + sinTheta * vec.y,
                                -sinTheta * vec.x + cosTheta * vec.y);
        }

        // Check if rectangle is placeable in cell at angle using early stopping
        private bool checkRectanglePlaceability(Vector2 rect, Vector2Int cell, float angle)
        {
            // compute number of steps
            float stepsize = resolution / 2;
            Vector2Int n_steps = Vector2Int.RoundToInt(2 * rect / stepsize + Vector2.one);

            // local object to floor transform and [m] to grid units
            Vector2 rect_rot = rotate(rect, angle) / resolution;
            Vector2 right_rot = rotate(Vector2.right, angle) / resolution;
            Vector2 up_rot = rotate(Vector2.up, angle) / resolution;

            // initiallize loop variables
            Vector2 sample;
            Vector2Int index;
            int sample_counter = 0;

            // start with outer corner of rectangle and iterate n_steps with stepsize
            // check corners and midpoints first: 9x9 grid over rectangle
            sample = cell - rect_rot;   // start with lower left corner
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    index = Vector2Int.RoundToInt(sample);
                    sample += up_rot * rect.y; // stepsize=rect.y
                    if (index.x < 0 || size.x <= index.x    // x out of bounds
                        || index.y < 0 || size.y <= index.y   // y out of bounds
                        || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                        return false;

                    sample_counter++;
                }
                sample += right_rot * rect.x; // stepsize=rect.x
                sample -= 3 * up_rot * rect.y; // n_steps.y=3, stepsize=rect.y
            }


            // check borders: sample circumference with steps size of resolution 
            // check left border
            sample = cell - rect_rot; // start with lower left corner
            for (int i = 0; i < n_steps.y; i++)
            {
                index = Vector2Int.RoundToInt(sample);
                sample += up_rot * stepsize;
                if (index.x < 0 || size.x <= index.x    // x out of bounds
                    || index.y < 0 || size.y <= index.y   // y out of bounds
                    || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                    return false;

                sample_counter++;
            }

            // check upper border
            for (int i = 0; i < n_steps.x; i++)
            {
                index = Vector2Int.RoundToInt(sample);
                sample += right_rot * stepsize;
                if (index.x < 0 || size.x <= index.x    // x out of bounds
                    || index.y < 0 || size.y <= index.y   // y out of bounds
                    || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                    return false;

                sample_counter++;
            }

            // check right border
            for (int i = 0; i < n_steps.y; i++)
            {
                index = Vector2Int.RoundToInt(sample);
                sample -= up_rot * stepsize;
                if (index.x < 0 || size.x <= index.x    // x out of bounds
                    || index.y < 0 || size.y <= index.y   // y out of bounds
                    || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                    return false;

                sample_counter++;
            }

            // check lower border
            for (int i = 0; i < n_steps.x; i++)
            {
                index = Vector2Int.RoundToInt(sample);
                sample -= right_rot * resolution;
                if (index.x < 0 || size.x <= index.x    // x out of bounds
                    || index.y < 0 || size.y <= index.y   // y out of bounds
                    || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                    return false;

                sample_counter++;
            }

            // check inside: sample area with steps size of resolution 
            sample = cell - rect_rot; // start with lower left corner
            for (float i = 0; i < n_steps.x; i++)
            {
                for (int j = 0; j < n_steps.y; j++)
                {
                    index = Vector2Int.RoundToInt(sample);
                    sample += up_rot * stepsize;
                    if (index.x < 0 || size.x <= index.x    // x out of bounds
                        || index.y < 0 || size.y <= index.y   // y out of bounds
                        || walkableGrid[index.x, index.y] != 0)  // is not walkable 
                        return false;

                    sample_counter++;
                }
                sample += right_rot * stepsize;
                sample -= n_steps.y * up_rot * stepsize;
            }

            return true;
        }

        #endregion Private Helper Functions

        private string queue2str<T>(Queue<T> queue)
        {
            string queue_str = "";
            for (int i = 0; i < queue.Count; i++)
            {
                T val = queue.Dequeue();
                queue_str += val + " <- ";
                queue.Enqueue(val);
            }
            return queue_str;
        }

        private string distGrid2str(float[,] grid, Vector2Int focus_cell)
        {
            string grid_str = "";
            int size_x = grid.GetLength(0);
            int size_y = grid.GetLength(0);

            for (int i = 0; i < size_x; i++)
            {
                for (int j = 0; j < size_y; j++)
                {
                    string val_str = "";
                    float val = grid[i, j];

                    // transform value to string
                    if (val == float.PositiveInfinity)
                        val_str += "-.-";
                    else
                        val_str += (val * 10).ToString("0.0");

                    // highlight focus cell
                    if (focus_cell.x == i && focus_cell.y == j)
                        val_str = "<" + val_str + ">";

                    // append to row
                    grid_str += val_str + '\t';
                }
                grid_str += "\n\n";     // start new row
            }
            return grid_str;
        }
    }
}