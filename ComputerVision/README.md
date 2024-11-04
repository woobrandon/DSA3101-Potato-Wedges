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

### How to run data_ingestion.py
1. Ensure that you have the driver file installed in the current directory. If you do not have chrome installed on your device, installed the neccssary driver:<br>
**Firefox**: https://github.com/mozilla/geckodriver/releases<br>
**Safari**: 
- Go to **Perferences** in **Safari**
- click on **Advanced** tab
- Check the option that says **"Show Develop menu in menu bar"**
- From **Develop** menu in menu bar, select **"Allow Remote Automation"**

2. Install the neccessary libraries by running the command in the backend directory:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the python script

If you see an error in the terminal that states the model file can not be located, change the directory to the backend folder and try again.

### Data Ingestion
The data from the amazon csv file is relatively clean but unfortunately, the image link for most of the products are damaged. To get the neccessary images, we have to scrape from the amazon website using the product link. Using the product link alone to scrape the image is not suffficient as Amazon has set up anti-bots detection features and has a list of pages third parties are allowed and not allowed tos scrape from (https://www.amazon.com/robots.txt). To circumvent this, scraping the website requires the use of a chrome driver to simulate accessing the website like a real user. Selenium The scraped images are saved in a folder titled "/amazon_images/", with the name of each image following the format "image_{row number}.jpg".

### Database
A database named "feature_database.db" is created For easy and efficient access to the data with the primary key being the id.

| Column Name   | Type  |
|---------------|-------|
| id            | INT   |
| product_id    | TEXT  |
| product_name  | TEXT  |
| product_price | FLOAT | 
| filename      | TEXT  |
| features      | BLOB  |
| productUrl    | TEXT  |
| about_product | TEXT  |
| category      | TEXT  |
| product_desc  | TEXT  |
| tokens        | BLOB  |
| lemma         | BLOB  |
| vector        | BLOB  |

Each column represents a specific attribute of a product, where:
- **`id`** is the unique identifier for each entry.
- **`product_id`** is a text identifier for the product.
- **`product_name`** and **`product_desc`** provide details about the product.
- **`features`, `tokens`, `lemma`,** and **`vector`** store additional data used for analysis and searching.

### Model
For our project, we used ResNet50, a deep convolutional neural network, to extract the features from the images. The model contains 50 layers, 48 convolutionaery layers and 2 connected layers. The model takes in the PIL image object and outputs a 1D vector. The pretrained model "resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5" is used in our project for its desirable properties:
- **`resnet50`**: The model is lightweight with only 50 years which enable us to run it locally withtout performance deficiencies.
- **`tf`**: The weights are compatible with the TensorFlow library.
- **`notop`**: The file excludes the weights for the final convolutional layers which is commonly used to image classification. For feature extraction, the final layer is excluded to return a feature vector.

#### Why do we use a CNN model instead of using the raw PIL?
Raw PIL does not effectively capture high level patterns like shapes and objects. ResNet50 captures the important features of an image and express it in a fixed-length vector which is useful for us to compare images later.

### Similar Images
To determine the similarity between 2 images, the cosine similarity is calculated between the 2 images. Cosine Similarity, like its name suggests, is the cosine of two non-zero vectors (in this case the image feature vectors) derived using the Euclidean dot product formula:

$$
\mathbf{A} \cdot \mathbf{B} = \|\mathbf{A}\| \|\mathbf{B}\| \cos \theta
$$

2 proportional vectors (similar images) have a cosine similarity of 1, whereas 2 othorgonal vectors (different images) have a cosine value of 0. 

Each image cosine similarity score is calculated with the uploaded image and sorted in descending order. An image below a certain threshold (0.8 for our project) is deemed as visually contrasting. This ensure that if the uploaded image does not visually look similar to an amazon product, no images will be return.

### How to run webpage

1. Ensure all the neccessary libraries are installed. Otherwise, Running the command in the backend directory:
   ```sh
   pip install -r requirements.txt
   ```

2. If npm is not installed in the local environment or local desktop,
For Windows:
- Go to https://nodejs.org/en to install Node.js
For Mac:
- run (if you have Homebrew):
   ```sh
   brew install node
   ```
- Verfiy installation by running the command:
   ```sh
   node -v
   npm -v
   ```

3. Run the app.py found in the ./ComputerVision/backend/ folder.

4. Run the command in a separate terminal at the directory ./ComputerVision/frontend/src
   ```sh
   npm start
   ```
5. Go to your brower of choice and type localhost:3000 to see the webpage