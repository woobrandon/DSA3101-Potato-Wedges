# Enchancing product descriptions and SEO

## LLM (Optimising product descriptions)

By leveraging on llama3, we can post a product description to an endpoint and recieve the enhanced version of the product description.

1. Install docker onto your local computer

2. Navigate to the LLM folder and run:

   ```sh
   cd ./LLM
   docker compose up
   ```

3. Ensure that the docker contains are up and running via docker desktop

4. Open up the application on your browser and enter the URL
   `http://localhost:5001/`

## Impact on search rankings and conversion rates using SEO

### Search Engine Optimisation

1. Content creation and optimisation

   - Analyse current trends and keywords by using tools like google analytics
   - Generate content using LLM by providing these analysis as context for improved visibility to products

2. Competitor Analysis

   - Using webscraping, analyse competitor content with LLM to identify areas that work well

3. Personalisation and Recommendations

   - Using user behaviour and preferences such as clicks, time spent on pages and purchase history, we can use AI to provide better recommendations and improve user engagement

### Analysis of impact

1. Performance tracking

   - Monitor the changes in search rankings and conversion rates after implementation and look for patterns
   - Compare the performance of the 2 versions using A/B testing

2. User engagement metrics

   - Evaluate sentiment of customers viewing content by analysing:
     - Comments
     - Reviews
     - Time spent on page
     - Page views
     - Transactions
     - Bounce rates
