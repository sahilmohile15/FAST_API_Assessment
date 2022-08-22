from sqlalchemy.orm import Session

import models
import schemas


class AddressRepo:
    
    async def create(db: Session, address: schemas.AddCreate):
        db_item = models.Address(name=address.name,address=address.address,address_point=address.address_point)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def fetch_by_id(db: Session,_id):
        return db.query(models.Address).filter(models.Address.id == _id).first()

    # def fetch_by_name(db: Session,name):
    #     return db.query(models.Address).filter(models.Address.name == name).first()

    def fetch_by_address(db: Session,add):
        return db.query(models.Address).filter(models.Address.address_point == add).first()
    
    def fetch_all(db: Session):
        return db.query(models.Address).order_by(models.Address.name)


    async def delete(db: Session,address_id):
        db_item= db.query(models.Address).filter_by(id=address_id).first()
        db.delete(db_item)
        db.commit()
        
    async def update(db: Session,data):
        updated_item = db.merge(data)
        db.commit()
        return updated_item
     