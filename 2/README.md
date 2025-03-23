| Model          | Unfozen layers | Batch Size | Learning Rate | Pre-training epochs | Fine-tuning epochs | Pre-training val accuracy | Fine-tuning val accuracy | Val accuracy difference | Pre-training val loss | Fine-tuning val loss | Val loss diffrence | 
|----------------|----------------|------------|---------------|---------------------|--------------------|---------------------------|--------------------------|-------------------------|-----------------------|----------------------|--------------------|
| ResNet50       | 10             | 16         | 1e-5          | 31                  | 11                 | 0.61                      | 0.8                      | 0.19                    | 0.65                  | 0.42                 | -0.23              | 
| ResNet101      | 20             | 16         | 1e-5          | 33                  | 6                  | 0.61                      | 0.79                     | 0.18                    | 0.66                  | 0.44                 | -0.22              | 
| Xception       | 20             | 12         | 1e-5          | 8                   | 20                 | 0.77                      | 0.99                     | 0.22                    | 0.48                  | 0.02                 | -0.46              | 
| EfficientNetB0 | 25             | 16         | 1e-5          | 6                   | 4                  | 0.5                       | 0.54                     | 0.04                    | 0.69                  | 0.69                 | 0                  | 
| EfficientNetB3 | 25             | 8          | 1e-5          | 5                   | 4                  | 0.52                      | 0.58                     | 0.06                    | 0.69                  | 0.67                 | -0.02              |

## Grafy:
### Porovnanie modelov:
![models_comparsion_histogram](https://github.com/user-attachments/assets/486831cb-ce56-47e3-bedb-74be89491fb6)

![resnet50_graphs](https://github.com/user-attachments/assets/a112f0da-0c9b-4464-b02d-88f8d4a3eea7)
![resnet101_graphs](https://github.com/user-attachments/assets/88cde356-d731-41f7-aecf-a4440ae64dff)
![xception_graphs](https://github.com/user-attachments/assets/166cf47b-beb7-4f7b-a8a0-9d748e832c13)
![efficientnetb0_graphs](https://github.com/user-attachments/assets/8a3bc6fa-c486-402e-90fc-96ac61df1d8c)
![efficientnetb3_graphs](https://github.com/user-attachments/assets/d86e3e08-e524-4068-b2ca-bd12221da632)
