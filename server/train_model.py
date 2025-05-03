import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

def load_and_preprocess_data(filename='hand_signs_dataset.json'):
    print("Loading dataset...")
    with open(filename, 'r') as f:
        dataset = json.load(f)
    
    print(f"Dataset size: {len(dataset)} samples")
    
    # Extract features and labels
    X = np.array([sample['features'] for sample in dataset])
    y = np.array([sample['label'] for sample in dataset])
    
    print(f"Unique labels: {np.unique(y)}")
    print(f"Feature shape: {X.shape}")
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save scaler for inference
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    y_onehot = to_categorical(y_encoded)
    
    print(f"Number of classes: {len(label_encoder.classes_)}")
    print(f"Classes: {label_encoder.classes_}")
    
    # Save label encoder
    with open('label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)
    
    return X_scaled, y_onehot, label_encoder

def create_model(input_shape, num_classes):
    model = Sequential([
        # Input layer
        Dense(512, input_shape=(input_shape,)),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(negative_slope=0.1),
        Dropout(0.3),
        
        # Hidden layers
        Dense(1024),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(negative_slope=0.1),
        Dropout(0.4),
        
        Dense(512),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(negative_slope=0.1),
        Dropout(0.3),
        
        Dense(256),
        BatchNormalization(),
        tf.keras.layers.LeakyReLU(negative_slope=0.1),
        Dropout(0.2),
        
        # Output layer
        Dense(num_classes, activation='softmax')
    ])
    
    # Fixed learning rate
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model():
    print("Starting training process...")
    X, y, label_encoder = load_and_preprocess_data()
    
    # Split data with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y.argmax(axis=1)
    )
    
    print("\nCreating model...")
    model = create_model(X_train.shape[1], y.shape[1])
    model.summary()
    
    # Add callbacks
    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            'best_model.keras',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    print("\nTraining model...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=200,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    # Evaluate on test set
    print("\nEvaluating model...")
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {test_acc:.4f}")
    
    # Generate predictions
    y_pred = model.predict(X_test)
    y_true = y_test.argmax(axis=1)
    y_pred_classes = y_pred.argmax(axis=1)
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(
        y_true,
        y_pred_classes,
        target_names=label_encoder.classes_
    ))
    
    # Save confusion matrix
    plt.figure(figsize=(15, 15))
    cm = confusion_matrix(y_true, y_pred_classes)
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=label_encoder.classes_,
        yticklabels=label_encoder.classes_
    )
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.savefig('confusion_matrix.png')
    plt.close()
    
    # Save training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.close()
    
    # Save final model
    model.save('hand_sign_model.keras')
    print("\nModel saved as 'hand_sign_model.keras'")

if __name__ == '__main__':
    train_model() 