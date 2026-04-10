from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question : str
    
class QueryResponse(BaseModel):
    answer : str
    
class GradeDocuments(BaseModel):
    """Boolean score for relevance check on retrieved documents."""
    
    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )