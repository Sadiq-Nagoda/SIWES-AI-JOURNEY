import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

                            #Reading Students records
base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir,"students_records.csv"))

def check_data_types(df):
    student_id_is_int = pd.api.types.is_integer_dtype(df["Student_ID"])
    if not student_id_is_int:
        raise ValueError("Student ID is invalid")
    
    name_is_valid = pd.api.types.is_string_dtype(df["Full_Name"])
    if not name_is_valid:
        raise ValueError("Invalid Name")
    scores_is_valid = (
    pd.api.types.is_integer_dtype(df["CA1"]) and
    pd.api.types.is_integer_dtype(df["CA2"]) and
    pd.api.types.is_integer_dtype(df["Exam"])
)
    if not scores_is_valid:
        print("The scores Are invalid")
def handle_missing_values(df):
            if df.isna().any().any():
                print("Fill The Missing Values")
                raise ValueError("The dataset contains missing values.")
def check_value_ranges(df):

    invalid_CA = df[((df[["CA1", "CA2"]] > 20) | (df[["CA1", "CA2"]] < 0)).any(axis=1)]
    if not invalid_CA.empty:
        print("Invalid CA1/CA2 rows:")
        print(invalid_CA)
        raise ValueError("Invalid CA1/CA2 scores found")

    invalid_exam = df[(df["Exam"] > 60) | (df["Exam"] < 0)]
    if not invalid_exam.empty:
        print("Invalid Exam rows:")
        print(invalid_exam)
        raise ValueError("Invalid Exam scores found")
def Total(df):
     df["Total"] = df["CA1"] + df["CA2"] + df["Exam"] 
def calculate_average(df):
     df["Average"] = df[["CA1","CA2","Exam"]].mean(axis=1)
def get_grade(Total):
    if Total >= 70:
        return "A"
    elif Total >= 60:
        return "B"
    elif Total >= 50:
        return "C"
    elif Total >= 45:
        return "D"
    else:
        return "F"
def assign_position(df):

     df["Position"] = df["Total"].rank(ascending=False).astype(int)
def display_results(df):
     print(df)
def turn_to_pdf(df):

    # Create PDF document
    pdf = SimpleDocTemplate("final_result.pdf")

    # Convert DataFrame to list
    data = [df.columns.tolist()] + df.values.tolist()

    # Create table
    table = Table(data)

    # Style the table
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    # Build PDF
    pdf.build([table])

    print("PDF file created successfully!")
     


                            #Validating the Data
    #cheking Required Columns
column_list = df.columns.to_list()
column_list_2 = ["Student_ID","Full_Name","CA1","CA2","Exam"]
if (column_list_2) == (column_list):
    #check missing values
    empty = df.isna().any().any()
    #Any missing Values?
    if empty == False:
        check_data_types(df)
        check_value_ranges(df)
        print("###############*************VALIDATION SUCCESSFUL******************######################")
    else:
        handle_missing_values(df)
else:
     missing_column = [item for item in column_list if item not in column_list_2]
     raise ValueError(missing_column)


print("**********************************************STUDENT SCORES*************************************")



check_data_types(df)
handle_missing_values(df)
check_value_ranges(df)
Total(df)
calculate_average(df)
df["Grade"] = df["Total"].apply(get_grade)
assign_position(df)
display_results(df)
turn_to_pdf(df)







        









