from apps.db.session import session
from passlib.hash import pbkdf2_sha256


def make_password(raw_password: str) -> str:
    return pbkdf2_sha256.hash(raw_password)
    

def check_password(hash: str, raw_password: str) -> str:
    return pbkdf2_sha256.verify(raw_password, hash)


def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()
        

class Database(object):
    
    def __init__(self,db,model) -> None:
        self.db = db
        self.model = model
    
    def get_by_any(self,**kwargs):
        return self.db.query(self.model).filter_by(**kwargs).first()
    
    def create(self,**kwargs):
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj



'''
def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return self._update_db(db, db_obj)

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return self._update_db(db, db_obj)

    def _update_db(self, db, db_obj):
        self._extracted_from_get_or_create_2(db, db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    # Get or Create Function
    def get_or_create(self, db: Session, **kwargs) -> ModelType:
        instance = db.query(self.model).filter_by(**kwargs).first()
        if not instance:
            instance = self.model(**kwargs)
            self._extracted_from_get_or_create_2(db, instance)
        return instance

    def _extracted_from_get_or_create_2(self, db, arg1):
        db.add(arg1)
        db.commit()
        db.refresh(arg1)

    def get_by_any(self, db: Session, **kwargs) -> ModelType:
        return db.query(self.model).filter_by(**kwargs).first()

    # Filter Function
    def filter(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order_by: any = None,
        **kwargs
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter_by(**kwargs)
            .order_by(order_by)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_or_update(
        self,
        db: Session,
        *,
        obj_create: CreateSchemaType,
        obj_update: UpdateSchemaType,
        id: str
    ) -> ModelType:
        try:
            instance = db.query(self.model).filter(self.model.uid == id).first()
        except Exception:
            instance = None
        if instance:
            return self.update(db, db_obj=instance, obj_in=obj_update)
        else:
            return self.create(db, obj_in=obj_create)

    def create_or_delete(
        self, db: Session, *, obj_create: CreateSchemaType, id: str
    ) -> ModelType:
        instance = db.query(self.model).filter(self.model.uid == id).first()
        if instance:
            return self.remove(db, id=instance.id)
        else:
            return self.create(db, obj_in=obj_create)

    def create_or_update_on_id(
        self,
        db: Session,
        *,
        obj_create: CreateSchemaType,
        obj_update: UpdateSchemaType,
        id: int
    ) -> ModelType:
        instance = db.query(self.model).filter(self.model.id == id).first()
        if instance:
            return self.update(db, db_obj=instance, obj_in=obj_update)
        else:
            return self.create(db, obj_in=obj_create)

    def create_or_update_by_any(
        self,
        db: Session,
        *,
        obj_create: CreateSchemaType,
        obj_update: UpdateSchemaType,
        **kwargs
    ) -> ModelType:
        instance = db.query(self.model).filter_by(**kwargs).first()
        if instance:
            return self.update(db, db_obj=instance, obj_in=obj_update)
        else:
            return self.create(db, obj_in=obj_create)

    def create_or_delete_by_any(
        self, db: Session, *, obj_create: CreateSchemaType, **kwargs
    ) -> ModelType:
        instance = db.query(self.model).filter_by(**kwargs).first()
        if instance:
            return self.remove(db, id=instance.id)
        else:
            return self.create(db, obj_in=obj_create)
'''