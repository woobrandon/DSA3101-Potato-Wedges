# Product Search, Discovery and Recommendation

## Computer vision for search and discovery & AI product recommendation (cross selling)

1. Install docker onto your local computer

2. Navigate to the LLM folder and run:

   ```sh
   cd ./ComputerVision
   docker compose up
   ```

3. Ensure that the docker contains are up and running via docker desktop

4. Open up the application on your browser by entering the URL

   `http://localhost:3000/`

5. Input an image and click on 'Find Product'

6. (Product Finder) Wait for the image to be processed and a list of products will appear for:

   - Products that look the same

   - Products that have a similar description

7. (Product Categorisation) Wait for the image to be processed and the category of the product will be shown

# Using computer vision techniques to enhance product search and discovery

To find visually similar products from the amazon dataset, we use a pretrained computer vision model ResNet 50 is used to find images with the most similarity

### Data Ingestion
The data from the amazon csv file is relatively clean but unfortunately, the image link for most of the products are damaged. To get the neccessary images, we have to scrape from the amazon website using the product link. Using the product link alone to scrape the image is not suffficient as Amazon has set up anti-bots detection features and has a list of pages third parties are allowed and not allowed tos scrape from (https://www.amazon.com/robots.txt). To circumvent this, scraping the website requires the use of a chrome driver to simulate accessing the website like a real user. Selenium The scraped images are saved in a folder titled "/amazon_images/", with the name of each image following the format "image_{row number}.jpg".

### Database
A database named "feature_database.db" is created For easy and efficient access to the data with the primary key being the id.

+--------------+-------+
| Column Name  | Type  |
+--------------+-------+
| id           | INT   |
| product_id   | TEXT  |
| product_name | TEXT  |
| product_price| FLOAT | 
| filename     | TEXT  |
| features     | BLOB  |
| productUrl   | TEXT  |
| about_product| TEXT  |
| category     | TEXT  |
| product_desc | TEXT  |
| tokens       | BLOB  |
| lemma        | BLOB  |
| vector       | BLOB  |
+--------------+-------+
