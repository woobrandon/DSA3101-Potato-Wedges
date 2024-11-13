# E-commerce Performance Analysis and Optimisation

## Overview

The Google Analytics sample dataset provides a comprehensive view of e-commerce performance data, specifically for the Google Merchandise Store, which sells Google-branded products. This dataset is typically used for analysis and experimentation with Google Analytics 360 data, offering insights into website traffic, user behavior, and transaction activities on an e-commerce platform.

The Google Analytics sample dataset is a rich resource for analyzing the performance of an e-commerce website, helping businesses and analysts optimize their marketing strategies, improve user experiences, and increase sales. By working with this dataset, we can explore how different traffic sources, content engagement, and product offerings impact overall store performance.

Since the Google Analytics sample dataset is an example of Google Analytics 360, the insights and analysis techniques derived from this data are directly applicable to any other e-commerce platform using Google Analytics 360. This means that businesses operating on different e-commerce websites can conduct similar analyses, such as understanding customer behavior, measuring sales performance and even managing inventories. With any other type of e-commerce platform, the structure and metrics in the Google Analytics 360 data remain consistent across sites.

## Set-up

1. Install the libraries used in our notebooks

   ```
   pip install -r requirements.txt
   ```

2. Using Google BigQuery requires additional set-up found here

   https://cloud.google.com/python/docs/reference/bigquery/latest

3. For LLM/Computer Vision models, navigate to their directories and run

   ```
   docker compose up
   ```

## Project structure

```
📦E-commerce Performance Analysis and Optimisation
 ┣ 📂ComputerVision
 ┃ ┗ 📜How can we use computer vision techniques to enhance product search and discovery?
 ┃   ┣ Develop an image-based search feature for visually similar products.
 ┃   ┗ Implement automatic product categorization based on image features.
 ┃
 ┣ 📂LLM
 ┃ ┗ 📜How can we leverage Large Language Models (LLMs) to enhance product descriptions and SEO?
 ┃   ┣ Develop a system using an LLM to generate optimized product descriptions.
 ┃   ┗ Analyze the impact of AI-generated content on search rankings and conversion rates.
 ┃
 ┣ 📂ProductRecommendation
 ┃ ┗ 📜How can we implement an AI-driven product recommendation system to increase cross-selling and upselling?
 ┃   ┣ Develop a collaborative filtering or content-based recommendation algorithm.
 ┃   ┗ Evaluate the impact of personalized recommendations on sales.
 ┃
 ┣ 📂Sentiment Analysis
 ┃ ┗ 📜What is the potential of using natural language processing to analyze customer reviews and feedback?
 ┃   ┣ Implement sentiment analysis on customer reviews.
 ┃   ┗ Identify common issues and suggestions from customer feedback.
 ┃
 ┣ 📂SubgroupA
 ┃ ┣ 📜What are the key factors influencing customer purchasing behavior?
 ┃ ┃ ┣ Analyze historical sales data to identify patterns and trends.
 ┃ ┃ ┗ Develop customer segmentation models based on purchasing behavior.
 ┃ ┣ 📜How can we improve customer retention and lifetime value?
 ┃ ┃ ┣ Calculate customer churn rates and identify at-risk customers.
 ┃ ┃ ┗ Analyze the effectiveness of current retention strategies.
 ┃ ┗ 📜What are the most effective marketing channels and campaigns?
 ┃   ┣ Evaluate the ROI of different marketing channels.
 ┃   ┗ Analyze the impact of various promotional campaigns on sales.
 ┃
 ┗ 📂SubgroupB
   ┣ 📂Q1
   ┃ ┗ 📜How can we optimize inventory levels to minimize costs while ensuring product availability?
   ┃   ┣ Develop a demand forecasting model using historical sales data.
   ┃   ┗ Create an inventory optimization algorithm to balance stock levels and costs.
   ┣ 📂Q2
   ┃ ┗ 📜What pricing strategies can we implement to maximize revenue?ensuring product availability?
   ┃   ┣ Analyze price elasticity for different product categories.
   ┃   ┗ Develop a dynamic pricing model based on demand and competition.
   ┗ 📂Q3
     ┗ 📜How can we improve the efficiency of our supply chain?ensuring product availability?
       ┣ Analyze supplier performance and identify bottlenecks.
       ┗ Optimize order fulfillment processes to reduce delivery times.
```

## Data dictionary

1. Google Analytics Sample Dataset

   https://support.google.com/analytics/answer/3437719?hl=en

2. Amazon sales dataset

   | **Section**                | **Sub-Section**         | **Attribute**         |
   | -------------------------- | ----------------------- | --------------------- |
   | **1. Product Information** | 1.1 Product ID          | `product_id`          |
   |                            | 1.2 Product Name        | `product_name`        |
   |                            | 1.3 Product Category    | `category`            |
   |                            | 1.4 Discounted Price    | `discounted_price`    |
   |                            | 1.5 Actual Price        | `actual_price`        |
   |                            | 1.6 Discount Percentage | `discount_percentage` |
   |                            | 1.7 Product Rating      | `rating`              |
   |                            | 1.8 Rating Count        | `rating_count`        |
   |                            | 1.9 Product Description | `about_product`       |
   | **2. User Reviews**        | 2.1 User ID             | `user_id`             |
   |                            | 2.2 User Name           | `user_name`           |
   |                            | 2.3 Review ID           | `review_id`           |
   |                            | 2.4 Review Title        | `review_title`        |
   |                            | 2.5 Review Content      | `review_content`      |
   | **3. Product Media**       | 3.1 Image Link          | `img_link`            |
   |                            | 3.2 Product Link        | `product_link`        |
