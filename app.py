# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import List
# from pymongo import MongoClient
# from llama_index import SimpleDirectoryReader, load_index_from_storage, VectorStoreIndex, StorageContext
# from llama_index.vector_stores.faiss import FaissVectorStore
# import os

# app = FastAPI()

# os.environ["OPENAI_API_KEY"] = "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"

# # Enable CORS for all domains (adjust as needed)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust to your frontend URL(s)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Connect to MongoDB
# client = MongoClient("mongodb+srv://shreyakhanna2k4:12345@cluster0.vq9fjgv.mongodb.net/?retryWrites=true&w=majority")
# db = client["prohunt"]
# collection = db["projects"]

# vector_store = FaissVectorStore.from_persist_dir("./storage")
# storage_context = StorageContext.from_defaults(
#     vector_store=vector_store, persist_dir="./storage"
# )
# index = load_index_from_storage(storage_context=storage_context)

# class ProjectInfo(BaseModel):
#     name: str
#     description: str
#     url: str

# @app.get("/api/projects/{query}")
# def search_projects(query: str) -> List[ProjectInfo]:
#     response = index.as_query_engine().query(query)
#     project_names = [project.split(". ")[1] for project in response.__dict__["response"].split("\n")[1:-1]]

#     project_infos = []

#     for project_name in project_names:
#         project_info = collection.find_one({"name": project_name}, {"_id": 0, "name": 1, "description": 1, "url": 1})

#         if project_info:
#             project_infos.append(ProjectInfo(**project_info))
#         else:
#             # Handle the case where information is not found for a project
#             print(f"Information not found for project: {project_name}")

#     return project_infos

# class VoteRequest(BaseModel):
#     project_id: str

# @app.post("/api/vote")
# async def vote_for_project(vote_request: VoteRequest):
#     project_id = vote_request.project_id

#     # Find the project in the database
#     existing_project = collection.find_one({"id": project_id})

#     if existing_project:
#         # Update the "votes" field for the specified project
#         collection.update_one({"id": project_id}, {"$inc": {"votes": 1}})
#         return {"message": "Vote recorded successfully"}

#     raise HTTPException(status_code=404, detail="Project not found")

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from llama_index import SimpleDirectoryReader, load_index_from_storage, VectorStoreIndex, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore
import os

app = FastAPI()

# Enable CORS for all domains (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend URL(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB
client = MongoClient(
    "mongodb+srv://shreyakhanna2k4:12345@cluster0.vq9fjgv.mongodb.net/?retryWrites=true&w=majority")
db = client.prohunt
collection = db.projects

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Load Llama index and vector store
vector_store = FaissVectorStore.from_persist_dir("./storage")
storage_context = StorageContext.from_defaults(
    vector_store=vector_store, persist_dir="./storage")
index = load_index_from_storage(storage_context=storage_context)


class UserInput(BaseModel):
    query: str


# async def search(query: str):
    # searching = query.query_params.get("query", "")
    # query = query.replace("%20",' ')
    # response = index.as_query_engine().query(query)
    # l = response.__dict__["response"].split("\n")
    # projects = [project.split(". ")[1] for project in l[1:-1]]
    # print(projects)
    # result = await collection.find({"name": {"$in": projects}})
    # return result

def search(query:str):
    query = query.replace("%20",' ')
    return query

@app.post("/api/projects")
async def root(user_input: UserInput):
    query = user_input.query
    response = index.as_query_engine().query(query)
    l = response.__dict__["response"].split("\n")
    print(l)
    result_cursor = collection.find({"name": {"$in": l}})
    return list(result_cursor)

# class VoteRequest(BaseModel):
#     project_id: str


# @app.post("/api/vote")
# async def vote_for_project(vote_request: VoteRequest):
#     project_id = vote_request.project_id

#     try:
#         # Find the project in the database
#         existing_project = collection.find_one({"id": project_id})

#         if existing_project:
#             # Update the "votes" field for the specified project
#             collection.update_one({"id": project_id}, {"$inc": {"votes": 1}})
#             return {"message": "Vote recorded successfully"}

#         raise HTTPException(status_code=404, detail="Project not found")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         raise HTTPException(status_code=500, detail="Internal server error")
