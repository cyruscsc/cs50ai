# Experiment Process

## Phase 1: Convolution & Pooling

Explore different numbers of convolution-pooling pairs with ascending numbers of filters.

### Model-1CP1DL

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9673 - loss 0.1389
- Testing: accuracy 0.9333 - loss 0.4875

### Model-2CP1DL

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9815 - loss 0.0691
- Testing: accuracy 0.9699 - loss 0.1600


### Model-3CP1DL

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9740 - loss 0.0978
- Testing: accuracy 0.9699 - loss 0.1733

### Observations

- Too few or too many convolution-pooling pairs may reduce accuracy
- [Model-2CP1DL](#model-2cp1dl) performs the best

## Phase 2: Dense Layer

Based on the best-performing model in the previous phase, explore different numbers of dense layers with ascending numbers of neurons.

### Model-2CP2DL

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9776 - loss 0.0821
- Testing: accuracy 0.9611 - loss 0.1850

### Model-2CP3DL

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9837 - loss 0.0655
- Testing: accuracy 0.9399 - loss 0.2488

### Observations

- Having more dense layers does not necessarily lead to better performance
- [Model-2CP1DL](#model-2cp1dl) still performs the best

## Phase 3: Dropout

Based on the best-performing model in the previous phase, explore different dropout rates.

### Model-2CP1DL2DO

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.9743 - loss 0.0931
- Testing: accuracy 0.9766 - loss 0.1099

### Model-2CP1DL5DO

```python
model = keras.models.Sequential([
    keras.layers.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
    keras.layers.Conv2D(16, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(32, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
])
```

- Training: accuracy 0.8715 - loss 0.4136
- Testing: accuracy 0.9454 - loss 0.2014

### Observations

- High dropout rate may reduce performance in both training and testing
- [Model-2CP1DL2DO](#model-2cp1dl2do) performs the best

## Best Model

[Model-2CP1DL2DO](#model-2cp1dl2do)
- 2 convolution layers (16 & 32 filters)
- 2 pooling layers (max pooling)
- 1 dense layer (128 neurons)
- 0.5 dropout rate
