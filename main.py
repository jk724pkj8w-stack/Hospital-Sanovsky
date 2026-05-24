from fastapi import FastAPI, Query, HTTPException, Header
from google.cloud import firestore
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from typing import Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.responses import JSONResponse
import json # Necesario para parsear la respuesta de verificar_correo

# --- Modelos Pydantic actualizados y nuevos ---

# Nuevo BaseModel para la creación de un nuevo paciente
# Ahora se espera el correo para vincularlo o crear un usuario
class NuevoPacienteData(BaseModel):
    nombre: str
    edad: int
    enfermedad: str
    correo: str # Campo crucial para vincular con el usuario

# Nuevo BaseModel para la creación de un nuevo usuario
class NuevoUsuarioData(BaseModel):
    nombre: str
    correo: str
    password: str 
    idUsuario: Optional[int] = None # Campo numérico, se gestiona internamente

# Cita model con todos los campos opcionales, y la opción de incluir datos para crear
class Cita(BaseModel):
    especialistaId: Optional[str] = Field(default=None, alias="especialistaId")
    pacienteId: Optional[str] = Field(default=None, alias="pacienteId") # ID de un paciente/usuario existente
    estado: Optional[str] = None
    fechaHora: Optional[datetime] = None
    fechaRegistro: Optional[datetime] = None
    motivo: Optional[str] = None
    nombreEspecialista: Optional[str] = None
    nombrePaciente: Optional[str] = None
    
    # Campos para crear un nuevo paciente/usuario si no existen
    crearNuevoPaciente: Optional[bool] = False
    datosNuevoPaciente: Optional[NuevoPacienteData] = None # Contiene el correo

# Clase para el modelo Paciente existente
class Paciente(BaseModel):
    nombre: str
    edad: int
    enfermedad: str
    # Si tus pacientes en Firestore tienen un campo para su ID de usuario, considéralo aquí
    # usuarioId: Optional[str] = None

class Usuario(BaseModel):
    nombre: str
    correo: str
    password: str 
    idUsuario: Optional[int] = None


# --- Configuración de la aplicación FastAPI y Firestore ---

load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if cred_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
else:
    raise RuntimeError("La variable de entorno GOOGLE_APPLICATION_CREDENTIALS no está definida.")

app = FastAPI()

# Firestore client
db = firestore.Client()

API_KEY = os.getenv("API_KEY", "secret123")

def validate_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints existentes (sin cambios significativos) ---

@app.get("/medicos")
def get_medicos():
    especialistas_ref = db.collection("especialistas")
    docs = especialistas_ref.stream()
    medicos = []
    for doc in docs:
        data = doc.to_dict()
        clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}
        medicos.append({"id": doc.id, **clean_data})
    return medicos

@app.get("/especialidadDetalle")
def get_especialidades():
    especialidades_ref = db.collection("especialidadDetalle")
    docs = especialidades_ref.stream()
    especialidades = []
    for doc in docs:
        data = doc.to_dict()
        clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}
        especialidades.append({"id": doc.id, **clean_data})
    return especialidades

@app.get("/especialidadDetalle/{id}")
def get_especialidad_detalle(id: str):
    doc_ref = db.collection("especialidadDetalle").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Especialidad no encontrada")
    data = doc.to_dict()
    clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}
    return {"id": doc.id, **clean_data}

@app.get("/pacientes")
def get_pacientes():
    pacientes_ref = db.collection("pacientes")
    docs = pacientes_ref.stream()
    pacientes = []
    for doc in docs:
        data = doc.to_dict()
        clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}
        pacientes.append({"id": doc.id, **clean_data})
    return pacientes

@app.post("/pacientes")
def add_paciente_manual(paciente: Paciente): # Renombrado para evitar conflicto con la lógica de add_cita
    paciente_dict = paciente.dict()
    doc_ref = db.collection("pacientes").add(paciente_dict)
    return {"message": "Paciente agregado", "id": doc_ref[1].id}

@app.get("/citas")
def get_citas(
    fecha_inicio: Optional[str] = Query(None, alias="fecha_inicio"),
    fecha_fin: Optional[str] = Query(None, alias="fecha_fin"),
    especialista_id: Optional[str] = Query(None, alias="especialista_id"),
    paciente_id: Optional[str] = Query(None, alias="paciente_id")
):
    citas_ref = db.collection("citas")
    if fecha_inicio:
        citas_ref = citas_ref.where("fecha", ">=", fecha_inicio)
    if fecha_fin:
        citas_ref = citas_ref.where("fecha", "<=", fecha_fin)
    if especialista_id:
        citas_ref = citas_ref.where("especialistaId", "==", especialista_id)
    if paciente_id:
        citas_ref = citas_ref.where("pacienteId", "==", paciente_id)
    docs = citas_ref.stream()
    citas = []
    for doc in docs:
        data = doc.to_dict()
        if "fechaHora" in data and hasattr(data["fechaHora"], "isoformat"):
            data["fechaHora"] = data["fechaHora"].isoformat()
        if "fecha" in data and hasattr(data["fecha"], "isoformat"):
            data["fecha"] = data["fecha"].isoformat()
        clean_data = {k: v for k, v in data.items() if isinstance(v, (str, int, float, bool, list, dict))}
        nombre_especialista = None
        if "especialistaId" in data:
            especialista_doc = db.collection("especialistas").document(data["especialistaId"]).get()
            if especialista_doc.exists:
                especialista_data = especialista_doc.to_dict()
                nombre_especialista = especialista_data.get("nombre")
        nombre_paciente = None
        if "pacienteId" in data:
            paciente_doc = db.collection("pacientes").document(data["pacienteId"]).get()
            if paciente_doc.exists:
                paciente_data = paciente_doc.to_dict()
                nombre_paciente = paciente_data.get("nombre")
        clean_data["nombreEspecialista"] = nombre_especialista
        clean_data["nombrePaciente"] = nombre_paciente
        citas.append({"id": doc.id, **clean_data})
    return citas

@app.get("/historial/{paciente_id}")
def get_historial_clinico(paciente_id: str):
    historial_ref = db.collection("historial_clinico").where("paciente_id", "==", paciente_id)
    docs = historial_ref.stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

@app.post("/historial")
def add_historial_clinico(entry: dict):
    paciente_id = entry.get("paciente_id")
    if not db.collection("pacientes").document(paciente_id).get().exists:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    doc_ref = db.collection("historial_clinico").add(entry)
    return {"message": "Entrada de historial clínico agregada", "id": doc_ref.id}

@app.put("/cita/{cita_id}")
def update_cita(cita_id: str, updated_data: dict, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    cita_ref = db.collection("citas").document(cita_id)
    if not cita_ref.get().exists:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita_ref.update(updated_data)
    return {"message": "Cita actualizada correctamente"}

@app.delete("/cita/{cita_id}")
def delete_cita(cita_id: str, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    cita_ref = db.collection("citas").document(cita_id)
    if not cita_ref.get().exists:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    cita_ref.delete()
    return {"message": f"Cita {cita_id} cancelada correctamente"}

@app.put("/doctor/{doctor_id}")
def update_doctor(doctor_id: str, updated_data: dict, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    doctor_ref = db.collection("doctores").document(doctor_id)
    if not doctor_ref.get().exists:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    doctor_ref.update(updated_data)
    return {"message": "Doctor actualizado correctamente"}

@app.delete("/doctor/{doctor_id}")
def delete_doctor(doctor_id: str, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    doctor_ref = db.collection("doctores").document(doctor_id)
    if not doctor_ref.get().exists:
        raise HTTPException(status_code=404, detail="Doctor no encontrado")
    doctor_ref.delete()
    return {"message": f"Doctor {doctor_id} eliminado correctamente"}

@app.put("/paciente/{paciente_id}")
def update_paciente(paciente_id: str, updated_data: dict, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    paciente_ref = db.collection("pacientes").document(paciente_id)
    if not paciente_ref.get().exists:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    paciente_ref.update(updated_data)
    return {"message": "Paciente actualizado correctamente"}

@app.delete("/paciente/{paciente_id}")
def delete_paciente(paciente_id: str, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    paciente_ref = db.collection("pacientes").document(paciente_id)
    if not paciente_ref.get().exists:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    paciente_ref.delete()
    return {"message": f"Paciente {paciente_id} eliminado correctamente"}

# ------------------- API CRUD para usuarios -------------------

@app.get("/usuarios")
def get_usuarios():
    usuarios_ref = db.collection("usuario")
    docs = usuarios_ref.stream()
    usuarios = []
    for doc in docs:
        data = doc.to_dict()
        usuarios.append({"id": doc.id, **data})
    return usuarios

@app.post("/usuarios")
def add_usuario_manual(usuario: Usuario): # Renombrado para evitar conflicto con la lógica interna
    # Verificar si el correo ya existe
    usuarios_ref = db.collection("usuario").where("correo", "==", usuario.correo)
    docs = list(usuarios_ref.stream())
    if docs:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    usuario_dict = usuario.dict()
    # Si idUsuario es numérico y lo quieres autoincrementar, deberías obtener el max_id aquí
    # Forzando un ID numérico secuencial si no se proporciona
    if usuario_dict.get("idUsuario") is None:
        ultimo_id = 0
        all_users = db.collection("usuario").stream()
        for doc in all_users:
            if "idUsuario" in doc.to_dict() and isinstance(doc.to_dict()["idUsuario"], int):
                ultimo_id = max(ultimo_id, doc.to_dict()["idUsuario"])
        usuario_dict["idUsuario"] = ultimo_id + 1

    doc_ref = db.collection("usuario").add(usuario_dict)
    return {"message": "Usuario agregado", "idUsuario": doc_ref[1].id}

@app.get("/usuarios/{usuario_id}")
def get_usuario(usuario_id: str):
    doc_ref = db.collection("usuario").document(usuario_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": doc.id, **doc.to_dict()}

@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: str, updated_data: dict, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    usuario_ref = db.collection("usuario").document(usuario_id)
    if not usuario_ref.get().exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_ref.update(updated_data)
    return {"message": "Usuario actualizado correctamente"}

@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: str, x_api_key: str = Header(...)):
    validate_api_key(x_api_key)
    usuario_ref = db.collection("usuario").document(usuario_id)
    if not usuario_ref.get().exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_ref.delete()
    return {"message": f"Usuario {usuario_id} eliminado correctamente"}


# --- Lógica de getValidaEmail modificada (sin cambios funcionales importantes, ya estaba bien) ---
@app.get("/getValidaEmail/{correo}")
def verificar_correo(correo: str):
    try:
        usuarios_ref = db.collection("usuario").where("correo", "==", correo)
        docs = usuarios_ref.stream()

        usuario_existente_doc_id = None
        for doc in docs:
            usuario_existente_doc_id = doc.id
            break

        ultimo_id_numerico = 0
        usuarios_all = db.collection("usuario").stream()
        for doc in usuarios_all:
            data = doc.to_dict()
            id_usuario_campo = data.get("idUsuario")
            if isinstance(id_usuario_campo, int) and id_usuario_campo > ultimo_id_numerico:
                ultimo_id_numerico = id_usuario_campo

        if usuario_existente_doc_id:
            return JSONResponse(content={
                "existente": True,
                "idUsuario": usuario_existente_doc_id
            })
        else:
            return JSONResponse(content={
                "existente": False,
                "siguienteIdNumerico": ultimo_id_numerico + 1
            })

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al verificar correo: {str(e)}")


# --- Lógica de add_cita modificada para crear usuario/paciente vinculado ---
@app.post("/cita")
def add_cita(cita: Cita):
    try:
        # 1. Validar Especialista (sin cambios)
        especialista_id_final = cita.especialistaId.strip() if cita.especialistaId else None
        if not especialista_id_final:
            raise HTTPException(status_code=400, detail="El ID del especialista no puede estar vacío.")

        especialista_doc = db.collection("especialistas").document(especialista_id_final).get()
        if not especialista_doc.exists:
            raise HTTPException(status_code=404, detail=f"Especialista con ID '{especialista_id_final}' no encontrado.")
        
        nombre_especialista = especialista_doc.to_dict().get("nombre")

        # 2. Determinar o Crear Paciente y Usuario Asociado
        final_paciente_id = None
        nombre_paciente = None

        if cita.crearNuevoPaciente:
            if not cita.datosNuevoPaciente:
                raise HTTPException(status_code=400, detail="Para crear un nuevo paciente, se deben proporcionar los 'datosNuevoPaciente'.")
            
            correo_paciente = cita.datosNuevoPaciente.correo
            if not correo_paciente:
                raise HTTPException(status_code=400, detail="El correo del nuevo paciente es obligatorio para vincularlo o crear un usuario.")

            # A. Buscar o Crear Usuario
            usuario_existente = db.collection("usuario").where("correo", "==", correo_paciente).limit(1).get()
            usuario_doc_id = None

            if usuario_existente:
                for doc in usuario_existente: # Solo debería haber uno debido al limit(1)
                    usuario_doc_id = doc.id
                    print(f"Usuario existente encontrado para '{correo_paciente}' con ID: {usuario_doc_id}")
                    break
            
            if not usuario_doc_id:
                # El usuario no existe, crearlo
                # Necesitamos un password. Podría ser un placeholder o generado.
                # En un sistema real, el sistema externo debería enviarlo o tener una lógica de generación.
                nuevo_usuario_data_dict = {
                    "nombre": cita.datosNuevoPaciente.nombre,
                    "correo": correo_paciente,
                    "password": "temp_auto_pass_123" # <<< IMPORTANTE: Gestionar esto adecuadamente
                }
                
                # Obtener el último idUsuario numérico para el nuevo usuario
                ultimo_id_numerico = 0
                usuarios_all = db.collection("usuario").stream()
                for doc in usuarios_all:
                    data = doc.to_dict()
                    id_usuario_campo = data.get("idUsuario")
                    if isinstance(id_usuario_campo, int) and id_usuario_campo > ultimo_id_numerico:
                        ultimo_id_numerico = id_usuario_campo
                nuevo_usuario_data_dict["idUsuario"] = ultimo_id_numerico + 1

                # Add con el ID de documento generado automáticamente por Firestore
                doc_ref_usuario = db.collection("usuario").add(nuevo_usuario_data_dict)
                usuario_doc_id = doc_ref_usuario[1].id # El ID del documento de Firestore recién creado
                print(f"Nuevo usuario '{correo_paciente}' creado con ID de documento: {usuario_doc_id}")

            # B. Usar el ID del documento del usuario como pacienteId y crear/actualizar el perfil de paciente
            final_paciente_id = usuario_doc_id # El ID del paciente será el mismo que el del usuario

            # Verificar si ya existe un perfil de paciente con este ID (es decir, el ID del usuario)
            paciente_perfil_existente = db.collection("pacientes").document(final_paciente_id).get()
            
            nuevo_paciente_data_to_store = cita.datosNuevoPaciente.dict(exclude={"correo"}) # Excluir correo aquí, ya está en el usuario
            nuevo_paciente_data_to_store["nombre"] = cita.datosNuevoPaciente.nombre # Asegurar que el nombre del paciente se guarda
            # Puedes añadir otros campos de NuevoPacienteData aquí
            # nuevo_paciente_data_to_store["usuarioId"] = usuario_doc_id # Opcional: para un enlace explícito

            if not paciente_perfil_existente.exists:
                # Si no existe el perfil de paciente, crearlo usando el ID del documento del usuario
                db.collection("pacientes").document(final_paciente_id).set(nuevo_paciente_data_to_store)
                print(f"Perfil de paciente creado para el ID de usuario '{final_paciente_id}'.")
            else:
                # Si ya existe, puedes optar por actualizarlo o dejarlo como está
                # Por ahora, simplemente confirmamos que existe.
                print(f"Perfil de paciente existente para el ID de usuario '{final_paciente_id}'. No se creará de nuevo.")
                # Si quisieras actualizar: db.collection("pacientes").document(final_paciente_id).update(nuevo_paciente_data_to_store)

            nombre_paciente = cita.datosNuevoPaciente.nombre # Usar el nombre del nuevo paciente
            
        else: # Si NO se indica crear un nuevo paciente, entonces pacienteId debe ser proporcionado y existir
            if not cita.pacienteId:
                raise HTTPException(status_code=400, detail="pacienteId no proporcionado y 'crearNuevoPaciente' es falso.")
            
            final_paciente_id = cita.pacienteId.strip()
            # Obtener nombre del paciente desde usuario si es necesario
            usuario_doc = db.collection("usuario").document(final_paciente_id).get()
            nombre_paciente = None
            if usuario_doc.exists:
                nombre_paciente = usuario_doc.to_dict().get("nombre", "Paciente sin nombre")
            else:
                nombre_paciente = "Paciente sin nombre"
            # Crear perfil de paciente si no existe
            paciente_doc = db.collection("pacientes").document(final_paciente_id).get()
            if not paciente_doc.exists:
                paciente_data = {
                    "nombre": nombre_paciente or "Paciente sin nombre",
                    "edad": 0,
                    "enfermedad": "No especificada"
                }
                db.collection("pacientes").document(final_paciente_id).set(paciente_data)
                print(f"Perfil de paciente creado automáticamente para el ID de usuario '{final_paciente_id}'.")
            else:
                # Si ya existe el perfil, obtener el nombre desde ahí si es posible
                nombre_paciente = paciente_doc.to_dict().get("nombre", nombre_paciente)
            print(f"Paciente '{nombre_paciente}' encontrado con ID: {final_paciente_id}")

        # 3. Construir el diccionario de la cita con los IDs y nombres finales
        cita_dict = {
            "especialistaId": especialista_id_final,
            "pacienteId": final_paciente_id, # Usar el ID final (del usuario)
            "estado": cita.estado,
            "fechaHora": cita.fechaHora,
            "fechaRegistro": cita.fechaRegistro or datetime.utcnow(),
            "motivo": cita.motivo,
            "nombreEspecialista": nombre_especialista,
            "nombrePaciente": nombre_paciente
        }

        # 4. Registrar la nueva cita
        doc_ref_cita = db.collection("citas").add(cita_dict)
        print(f"Cita registrada con ID: {doc_ref_cita[1].id}")
        return {"message": "Cita registrada", "id": doc_ref_cita[1].id}
        
    except HTTPException as http_exc:
        print(f"HTTPException en add_cita: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor al procesar la cita: {str(e)}")