# Enchancing product descriptions and SEO

## LLM (Optimising product descriptions)

1. Download the libraries required:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure that docker is also installed.

2. Pull and build the docker image, run the docker container and install llama3:

   ```sh
   sh -c DockerOllama.sh
   ```

   or

   ```bash
   bash DockerOllama.sh
   ```

3. Run the application and navigate to the exposed port:
   ```python
   python app.py
   ```
