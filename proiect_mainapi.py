from fastapi import FastAPI, Depends, HTTPException
from database import Product, ProductCreate, ProductResponse, ProductUpdate   
from sqlalchemy.orm import Session,sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from proiect_classes import Identifier,Country,ConsumerUnit,Ownership,Characteristic,Relationship,IdentifierCharacteristic
from proiect_classes import IdentifierCreate,IdentifierResponse,IdentifierUpdate,CountryCreate,CountryResponse,CountryUpdate

app = FastAPI()

from fastapi.responses import HTMLResponse

DATABASE_URL = 'mssql+pyodbc://GREEN/Proiect?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Pagina Mea</title>
        </head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1 style="color: #2e7d32;">Bun venit la Catalogul de Produse!</h1>
            <p>Serverul rulează corect și este conectat la SQL Server.</p>
            <hr>
            <a href="/docs" style="padding: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                Mergi la Documentație (Swagger)
            </a>
        </body>
    </html>
    """



@app.post("/Identifiers/", response_model=IdentifierResponse)
def create_identifier(identifier: IdentifierCreate, db: Session = Depends(get_db)):
    db_identifier = Identifier(**identifier.model_dump())
    db.add(db_identifier)
    db.commit()
    db.refresh(db_identifier)
    return db_identifier

@app.post("/Countries/", response_model=CountryResponse)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    db_country = Country(**country.model_dump())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

# @app.get("/products/", response_model=list[ProductResponse])
# def read_all_products(db: Session = Depends(get_db)):
#     products = db.query(Product).all()  
#     return products  

# @app.get("/products/{product_id}", response_model=ProductResponse)
# def read_product(product_id: int, db: Session = Depends(get_db)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product

# @app.put("/products/{product_id}", response_model=ProductResponse)
# def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     for key, value in product.model_dump().items():
#         setattr(db_product, key, value)
    
#     db.commit()
#     db.refresh(db_product)
#     return db_product

# @app.patch("/products/{product_id}", response_model=ProductResponse)
# def patch_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")

#     # Update only the fields that were provided in the request
#     if product_update.name is not None:
#         db_product.name = product_update.name
#     if product_update.description is not None:
#         db_product.description = product_update.description
#     if product_update.price is not None:
#         db_product.price = product_update.price

#     db.commit()
#     db.refresh(db_product)
#     return db_product

# @app.delete("/products/{product_id}")
# def delete_product(product_id: int, db: Session = Depends(get_db)):
#     db_product = db.query(Product).filter(Product.id == product_id).first()
#     if db_product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     db.delete(db_product)
#     db.commit()
#     return {"detail": "Product deleted"}
