# Set working directory
# First attemps to cd into .ci, if that fails try from one level up
cd .ci || cd DOMEXPipeline/.ci

# build and deploy
docker-compose build --build-arg AZURE_KEY=${AZURE_KEY} --build-arg AZURE_ENDPOINT=${AZURE_ENDPOINT};
docker-compose up -d;
