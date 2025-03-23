| Model          | Dropout | Batch Size | Learning Rate | Planned Epochs | Actual Epochs | Val Accuracy | Val Loss |
|----------------|---------|------------|---------------|----------------|---------------|--------------|----------|
| EfficientNetB0 | 0.3     | 16         | 1e-4          | 100            | 31            | 0.61         | 0.65     |
| EfficientNetB3 | 0.3     | 8          | 1e-4          | 100            | 33            | 0.61         | 0.66     |
| ResNet50       | 0.5     | 16         | 1e-4          | 100            | 7             | 0.77         | 0.48     |
| ResNet101      | 0.4     | 16         | 1e-4          | 100            | 6             | 0.5          | 0.69     |
| Xception       | 0.5     | 12         | 1e-4          | 100            | 5             | 0.52         | 0.69     |

Early stop bol aplikovaný na všetky modely, takže sa vypli dostatočne skoro

## Grafy
![efficientnetb3_graphs](https://github.com/user-attachments/assets/bbf79278-70db-4860-9ae7-8afe62f67f42)
![efficientnetb0_graphs](https://github.com/user-attachments/assets/08846691-9cec-462e-a185-d758f2a5e6c5)
![xception_graphs](https://github.com/user-attachments/assets/5cc413e2-2009-4f03-87cd-c3246ccc2955)
![resnet101_graphs](https://github.com/user-attachments/assets/5522e340-ca86-40c2-8562-cc9e601637a6)
![resnet50_graphs](https://github.com/user-attachments/assets/eb66d1dc-902c-4d47-b496-0fcd860420f9)
