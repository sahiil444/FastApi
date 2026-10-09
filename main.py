from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
        return data

@app.get("/")
def homepage():
    return {
        'massage' : 'Patient Management System'
    }

@app.get('/about')
def about():
    return {
        'massage' : 'A fully functional API to manage your patient records'
    }

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id : str = Path(..., description="Enter patient_id in the given formate",examples='P001')):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail="Patient_id not found")
    return data[patient_id]

@app.get('/sort')
def sort_patients(sort_by : str = Query(...,description="Sort on the basis of height,Weight or BMI"), order : str = Query('asc',description='sort in asc or desc')):
    required_sort_by = ['height','weight','bmi']
    required_order = ['asc','desc']

    if sort_by not in required_sort_by:
        raise HTTPException(status_code=400, detail=f"Sorting can be done on these columns {required_sort_by}")

    if order not in required_order:
        raise HTTPException(status_code=400, detail=f"orderinig can be in these formate {required_order}")

    data = load_data()
    sort_order = True if order == 'desc' else False 
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0), reverse=sort_order)

    return sorted_data