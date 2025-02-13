from database import engine, Base
import models

# cria todas as tabelas
models.Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso")
