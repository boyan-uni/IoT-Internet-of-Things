# Internet of Things - 基于云计算的物联网数据处理与预测系统 - 中英版项目介绍
Link to [CSC8112 Report1 Boyan Li (IoT).pdf](https://github.com/boyan-uni/IoT-Internet-of-Things/blob/master/CSC8112%20Report1%20Boyan%20Li%20(IoT).pdf)

## Introduction in English

### Project Description

- **Project Name**: Cloud-Based IoT Data Processing and Prediction System

- **Project Overview**: This project aims to develop a cloud-based Internet of Things (IoT) data processing and prediction system. The system continuously collects, processes, and predicts air quality data (specifically PM2.5) from a city observation platform. The project involves tasks such as data collection, preprocessing, time-series data prediction, and visualization. The entire process is deployed and managed using Docker container technology on the Azure cloud platform.

### Technology Stack

- The project was primarily developed using Python and deployed in a containerized environment on the Azure cloud platform utilizing Docker and Kubernetes. The system also integrates Prometheus and Grafana for monitoring and log management, ensuring system stability and maintainability.

### Achievements

- **Data Collection and Processing**:

  - Successfully designed and implemented a data injection component that captures real-time continuous PM2.5 data streams from the city observation platform via HTTP requests. The data is transmitted and processed in the cloud through RabbitMQ message queues. The data preprocessing module runs within a Docker container, filters out outliers exceeding 50, and calculates the daily average PM2.5 values.

- **System Optimization and Reliability**:

  - Optimized the data processing logic within the preprocessing phase, ensuring that all logic is executed within the main function of each file. This approach minimized errors caused by parameter passing. System efficiency was further improved by refining the code logic and ensuring the correct format of timestamps.

- **Time-Series Data Prediction and Visualization**:

  - Successfully predicted PM2.5 trends for the next 15 days using a machine learning model, with the results visualized using Matplotlib. The accuracy of the prediction model was enhanced, enabling the identification of trend change points and providing short-term forecasts of PM2.5 concentration levels.
  
- **Data Processing Efficiency**:

  - Reduced data processing time by 30% compared to the original approach, significantly enhancing system response speed.
  
- **Prediction Model Accuracy**:

  - Maintained an average error rate of less than 5% in predicting PM2.5 trends for the next 15 days, greatly improving the accuracy of the prediction model.



## 中文简介

### 项目描述

- 项目名称: 基于云计算的物联网数据处理与预测系统

- 项目概述: 该项目旨在开发一个基于云计算的物联网（IoT）数据处理与预测系统，系统通过持续收集、处理和预测来自城市观测平台的空气质量数据（主要是PM2.5）。项目涉及数据采集、预处理、时序数据预测与可视化等任务，整个流程在 Azure 云平台上使用 Docker 容器技术进行部署与管理。

### 技术栈

- 项目使用了Python进行主要开发，并在 Azure 云平台上利用 Docker、Kubernetes 进行容器化部署。系统还集成了 Prometheus 和 Grafana 进行监控和日志管理，确保系统的稳定性和可维护性。

### 成果描述

- **数据采集与处理**:

  - 成功设计并实现了数据注入组件，通过 HTTP 请求从城市观测平台实时捕捉持续的 PM 2.5 大数据流，并通过 RabbitMQ 消息队列在云端进行传输与处理。数据预处理模块在 Docker 容器中运行，过滤掉超过 50 的异常值，并计算每天的平均 PM2.5 值。

- **系统优化与可靠性**:

  - 在数据预处理部分，优化了数据处理逻辑，确保所有逻辑都在每个文件的主函数中执行，从而减少了由于参数传递引起的错误。通过改进代码逻辑和正确的时间戳格式，系统处理效率得到了提升。

- **时序数据预测与可视化**:

  - 使用机器学习模型成功预测未来 15 天的 PM2.5 趋势，预测结果通过 Matplotlib 进行可视化。模型预测的精度得到了提升，能够识别出趋势变化点，并提供短期内的 PM2.5 浓度变化预测。
  
- **数据处理效率**:

  - 每次数据处理的时间较原始方案缩短了 30% ，极大提高了系统的响应速度。
  
- **预测模型准确度**:

  - 未来 15 天 PM2.5 趋势预测的平均误差率控制在 5% 以内，显著提高了预测模型的准确性。
 
  
