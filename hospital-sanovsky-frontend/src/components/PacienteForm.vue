<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4 w-100" style="max-width: 600px;">
      <div v-if="mensajeExito" class="alert alert-success" role="alert">
        {{ mensajeExito }}
      </div>
      <div v-if="mensajeError" class="alert alert-danger" role="alert">
        {{ mensajeError }}
      </div>
      <form @submit.prevent="registrarPaciente">
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
          <label for="edad" class="form-label">Edad</label>
          <input type="number" id="edad" v-model="edad" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="alergias" class="form-label">Alergias</label>
          <input type="text" id="alergias" v-model="alergias" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="correo" class="form-label">Correo</label>
          <input type="email" id="correo" v-model="correo" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="direccion" class="form-label">Dirección</label>
          <input type="text" id="direccion" v-model="direccion" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="sexo" class="form-label">Sexo</label>
          <select id="sexo" v-model="sexo" class="form-select" required>
            <option value="Masculino">Masculino</option>
            <option value="Femenino">Femenino</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="telefono" class="form-label">Teléfono</label>
          <input type="text" id="telefono" v-model="telefono" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">Registrar Paciente</button>
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
      edad: '',
      alergias: '',
      correo: '',
      direccion: '',
      sexo: 'Masculino',
      telefono: '',
      mensajeExito: '',
      mensajeError: ''
    };
  },
  methods: {
    async registrarPaciente() {
      try {
        const docRef = await addDoc(collection(db, 'pacientes'), {
          apellidoPaterno: this.apellidoPaterno,
          apellidoMaterno: this.apellidoMaterno,
          nombre: this.nombre,
          edad: this.edad,
          alergias: this.alergias,
          correo: this.correo,
          direccion: this.direccion,
          sexo: this.sexo,
          telefono: this.telefono,
          idHospital: "/hospital/hospital_001",
          fechaRegistro: new Date()
        });
        console.log("Paciente registrado con ID: ", docRef.id);
        this.mensajeExito = 'Paciente registrado con éxito!';
        this.mensajeError = '';
        setTimeout(() => {
          this.mensajeExito = '';
        }, 3000);
        this.apellidoPaterno = '';
        this.apellidoMaterno = '';
        this.nombre = '';
        this.edad = '';
        this.alergias = '';
        this.correo = '';
        this.direccion = '';
        this.sexo = 'Masculino';
        this.telefono = '';
        this.$emit('paciente-registrado');
      } catch (e) {
        console.error("Error al registrar paciente: ", e);
        this.mensajeError = 'Ocurrió un error al registrar al paciente.';
        this.mensajeExito = '';
        setTimeout(() => {
          this.mensajeError = '';
        }, 5000);
      }
    }
  }
}
</script>