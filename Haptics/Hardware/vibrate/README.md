# Available commands

## Vibrate

### Description

Vibrates the whole device at the gait frequency.

### Usage

```bash
V <float:frequency>
```

## Tactor

### Description

Vibrates one tactor at the gait frequency.

### Usage

```bash
T <int:tactor_id> <float:frequency>
```

## Stop

### Description

Stops all vibrations.

### Usage

```bash
S
```

## Examples

```bash
V 1.0
```

Vibrates all tactors with a period of 1.0 second and a duty cycle of 50%.

```bash
T 1 1.0
```

Activates tactor 1 with a period of 1.0 second and a duty cycle of 50%.

```bash
S
```

Stops all vibrations.
