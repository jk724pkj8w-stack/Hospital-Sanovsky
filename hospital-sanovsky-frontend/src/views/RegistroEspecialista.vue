<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4 w-100" style="max-width: 600px;">
      <div v-if="mensajeExito" class="alert alert-success" role="alert">
        {{ mensajeExito }}
      </div>
      <div v-if="mensajeError" class="alert alert-danger" role="alert">
        {{ mensajeError }}
      </div>
      <form @submit.prevent="registrarEspecialista">
        <div class="mb-3">
          <label for="nombre" class="form-label">Nombre</label>
          <input type="text" id="nombre" v-model="nombre" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="apellidoPaterno" class="form-label">Apellido Paterno</label>
          <input type="text" id="apellidoPaterno" v-model="apellidoPaterno" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="apellidoMaterno" class="form-label">Apellido Materno</label>
          <input type="text" id="apellidoMaterno" v-model="apellidoMaterno" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="especialidad" class="form-label">Especialidad</label>
          <input type="text" id="especialidad" v-model="especialidad" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="titulo" class="form-label">Título</label>
          <input type="text" id="titulo" v-model="titulo" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="cedula" class="form-label">Cédula Profesional</label>
          <input type="text" id="cedula" v-model="cedula" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="correo" class="form-label">Correo</label>
          <input type="email" id="correo" v-model="correo" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="telefono" class="form-label">Teléfono</label>
          <input type="text" id="telefono" v-model="telefono" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Registrar Especialista</button>
      </form>
    </div>
  </div>
</template>

<script>
import { addDoc, collection } from 'firebase/firestore';
import { db } from '../firebase';

export default {
  data() {
    return {
      apellidoPaterno: '',
      apellidoMaterno: '',
      nombre: '',
      especialidad: '',
      titulo: '',
      cedula: '',
      correo: '',
      telefono: '',
      mensajeExito: '',
      mensajeError: ''
    };
  },
  methods: {
    async registrarEspecialista() {
      try {
        const docRef = await addDoc(collection(db, 'especialistas'), {
          apellidoPaterno: this.apellidoPaterno,
          apellidoMaterno: this.apellidoMaterno,
          nombre: this.nombre,
          especialidad: this.especialidad,
          titulo: this.titulo,
          cedula: this.cedula,
          correo: this.correo,
          telefono: this.telefono,
          fechaRegistro: new Date()
        });
        console.log("Especialista registrado con ID: ", docRef.id);
        this.mensajeExito = 'Especialista registrado con éxito!';
        this.mensajeError = '';
        setTimeout(() => {
          this.mensajeExito = '';
        }, 3000);
        this.apellidoPaterno = '';
        this.apellidoMaterno = '';
        this.nombre = '';
        this.especialidad = '';
        this.titulo = '';
        this.cedula = '';
        this.correo = '';
        this.telefono = '';
        this.$emit('especialista-registrado');
      } catch (e) {
        console.error("Error al registrar especialista: ", e);
        this.mensajeError = 'Ocurrió un error al registrar al especialista.';
        this.mensajeExito = '';
        setTimeout(() => {
          this.mensajeError = '';
        }, 5000);
      }
    }
  }
}
</script>