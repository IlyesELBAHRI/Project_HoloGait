using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FadeInElement : MonoBehaviour
{
    private Renderer meshRenderer;
    private Color initialColor;
    private Color targetColor;
    private float fadeDuration = 1.0f;

    private void Start()
    {
        meshRenderer = GetComponent<Renderer>();
        initialColor = meshRenderer.material.color;
        targetColor = new Color(initialColor.r, initialColor.g, initialColor.b, 0);
        meshRenderer.material.color = targetColor; // Initial transparency set to 0
        StartCoroutine(FadeIn());
    }

    private IEnumerator FadeIn()
    {
        float elapsedTime = 0;

        while (elapsedTime < fadeDuration)
        {
            float t = elapsedTime / fadeDuration;
            meshRenderer.material.color = Color.Lerp(targetColor, initialColor, t);
            elapsedTime += Time.deltaTime;
            yield return null;
        }

        meshRenderer.material.color = initialColor; // Ensure the final transparency is set to 1
    }
}

