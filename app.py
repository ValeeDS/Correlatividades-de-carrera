import pandas as pd

Materias = pd.read_excel('Correlatividades.xlsx', "Materias")
Cor_cursada = pd.read_excel('Correlatividades.xlsx', "Cursar", usecols = "C:CB",header=2)
Cor_final = pd.read_excel('Correlatividades.xlsx', "Aprobar", usecols = "C:CB",header=2)

class Task:
    def __init__(self, nombre, codigo, tipo, cor_cursada):
        self.nombre = nombre
        self.codigo = codigo
        self.tipo = tipo
        self.cor_cursada = cor_cursada
        self.cor_aprobar = []
        self.notas_parciales = []
        self.nota_cursada = 0
        self.nota_final = 0
        self.status = "Por cursar"

    def __repr__(self):
        return f"\n\n{self.nombre}\n-cod: {self.codigo},\n-estado: {self.status},\n-dependencies: {self.dependencies},\n-cursada: {self.nota_cursada},\n-final: {self.nota_final}"
    
class Task_manager:
    def __init__(self):
        self.tasks = []

    def add_task(self, nombre, codigo, tipo, cor_cursadas):
        task = Task(nombre, codigo, tipo, cor_cursadas)
        self.tasks.append(task)

    def get_task_by_id(self, codigo):
        for task in self.tasks:
            if task.codigo == codigo:
                return task
        return None
        
    def get_materias_para_cursar(self, tipo = "Todo"):
        materias_para_cursar = []
        for task in self.tasks:
            if tipo != "Todo":
                if task.status == "Por cursar" and task.tipo == tipo and self.correlativa_cursada_met(task):
                    materias_para_cursar.append(task.nombre)
            else:
                if task.status == "Por cursar" and self.correlativa_cursada_met(task):
                    materias_para_cursar.append(task.nombre)
        return materias_para_cursar

    def get_materias_para_rendir(self):
        materiar_para_rendir =[]
        for task in self.tasks:
            if task.status == "Cursada" and self.correlativa_final_met(task):
                materiar_para_rendir.append(task.nombre)
        return materiar_para_rendir
    
    def correlativa_cursada_met(self, task):
        for dependency in task.cor_cursada:
            dep_task = self.get_task_by_id(dependency[0])
            if dependency[1] == 'C' and (dep_task.status == "Cursada" or dep_task.status == "Aprobada"): met = True
            elif dependency[1] == 'A' and dep_task.status == "Aprobada": met = True
            else: met = False
            if dep_task is None or not met:
                return False
        return True
    
    def correlativa_final_met(self, task):
        for dependency in task.cor_aprobar:
            dep_task = self.get_task_by_id(dependency[0])
            if dependency[1] == 'C' and (dep_task.status == "Cursada" or dep_task.status == "Aprobada"): met = True
            elif dependency[1] == 'A' and dep_task.status == "Aprobada": met = True
            else: met = False
            if dep_task is None or not met:
                return False
        return True

    def change_status(self, codigo):
        task = self.get_task_by_id(codigo)
        if task is not None:
            final = task.nota_final
            cursada = task.nota_cursada
            if final > 3:
                task.status = "Aprobada"
            elif cursada > 3:
                task.status = "Cursada"
            else:
                task.status = "Por cursar"
            
    def change_nota_final(self, codigo, nota):
        task = self.get_task_by_id(codigo)
        if task is not None:
            task.nota_final = nota
            self.change_status(codigo)
        
    def change_nota_cursada(self, codigo, nota):
        task = self.get_task_by_id(codigo)
        if task is not None:
            task.nota_cursada = nota
            self.change_status(codigo)

    def assign_cor_cursada(self, codigo, cursar):
        task = self.get_task_by_id(codigo)
        if task is not None:
            task.cor_cursada = cursar
    
    def assign_cor_final(self, codigo, aprobar):
        task = self.get_task_by_id(codigo)
        if task is not None:
            task.cor_aprobar = aprobar
            
manager = Task_manager()
tareas = manager.tasks
for row in Materias.iterrows():
    manager.add_task(row[1]["Materia"].strip().replace('\n',' '),row[1]["Id"],row[1]["Tipo"],[])
    
for row in Cor_cursada.iterrows():
    row = row[1].dropna()
    dependencias = []
    if len(row.index.values) > 1:
        for _ in range(1,len(row.index.values)):
            dependencias.append((row.index.values[_],list(row)[_]))
        manager.assign_cor_cursada(row["Materia"],dependencias)

for row in Cor_final.iterrows():
    row = row[1].dropna()
    dependencias = []
    if len(row.index.values) > 1:
        for _ in range(1,len(row.index.values)):
            dependencias.append((row.index.values[_],list(row)[_]))
        manager.assign_cor_final(row["Materia"],dependencias)

manager.change_nota_cursada("CB37",8)
manager.change_nota_final("CB37",8)
manager.change_nota_final("CB03",8)
manager.change_nota_cursada("CB39",2)
manager.change_nota_cursada("CB39",5)
manager.change_nota_final("CB34",9)
manager.change_nota_final("CB01",7)
manager.change_nota_final("CB36",10)
manager.change_nota_cursada("CB29",7)
manager.change_nota_final("CB29",7)
manager.change_nota_cursada("CMP01",6)
manager.change_nota_cursada("CB13",1)
manager.change_nota_cursada("CB13",6)
manager.change_nota_cursada("CB10",7)
manager.change_nota_final("CB10",7)
manager.change_nota_cursada("CB40",8)
manager.change_nota_final("CB40",10)
manager.change_nota_final("CB02",10)
manager.change_nota_cursada("CB09",8)
manager.change_nota_cursada("CB05",7)
manager.change_nota_final("CB05",2)
manager.change_nota_final("CB05",2)
manager.change_nota_final("CB28",10)
manager.change_nota_final("CB06",10)
manager.change_nota_cursada("ELE78",8)

# print(tareas)

print(manager.get_materias_para_cursar("Normal"))
print(manager.get_materias_para_rendir())