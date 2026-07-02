# Prequiresuites
# First npm, docker, and docker daemon/hub must be install
# Docker daemon/hub must be running
# API KEYS inside ./api-gateway/.env must be given 
# For Tavily Search and Groq API

cd api-gateway

# do this if venv is not in the current dir of api-gateway
python3 -m venv venv
source venv/bin/activate


echo "Installing requirements ..."
# run this always 
pip install -r requirements.txt

# make a command to start a mongo db server
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongo_data:/data/db \
  mongo:latest



cd frontend
npm install
npm run dev