<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow p-4 w-100" style="max-width: 600px;">
      <div v-if="mensajeExito" class="alert alert-success" role="alert">
        {{ mensajeExito }}
      </div>
      <div v-if="mensajeError" class="alert alert-danger" role="alert">
        {{ mensajeError }}
      </div>
      <form @submit.prevent="registrarCita">
        <div class="mb-3">
          <label for="paciente" class="form-label">Paciente</label>
          <select id="paciente" v-model="pacienteId" class="form-select" required>
            <option disabled value="">Selecciona un paciente</option>
            <option v-for="p in pacientes" :key="p.id" :value="p.id">
              {{ p.nombre }} {{ p.apellidoPaterno }} {{ p.apellidoMaterno }}
            </option>
          </select>
          <div v-if="pacienteId">
            <p><strong>Paciente:</strong> {{ pacienteSeleccionado.nombre }} {{ pacienteSeleccionado.apellidoPaterno }} {{ pacienteSeleccionado.apellidoMaterno }}</p>
            <p><strong>Correo:</strong> {{ pacienteSeleccionado.correo }}</p>
          </div>
        </div>
        <div class="mb-3">
          <label for="especialista" class="form-label">Especialista</label>
          <select id="especialista" v-model="especialistaId" class="form-select" required>
            <option disabled value="">Selecciona un especialista</option>
            <option v-for="e in especialistas" :key="e.id" :value="e.id">
              {{ e.nombre }} {{ e.apellidoPaterno }} {{ e.apellidoMaterno }} - {{ e.especialidad }}
            </option>
          </select>
          <div v-if="especialistaId">
            <p><strong>Especialista:</strong> {{ especialistaSeleccionado.nombre }} {{ especialistaSeleccionado.apellidoPaterno }} {{ especialistaSeleccionado.apellidoMaterno }}</p>
            <p><strong>Especialidad:</strong> {{ especialistaSeleccionado.especialidad }}</p>
          </div>
        </div>
        <div class="mb-3">
          <label for="fechaHora" class="form-label">Fecha y Hora</label>
          <input type="datetime-local" id="fechaHora" v-model="fechaHora" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="motivo" class="form-label">Motivo de la cita</label>
          <input type="text" id="motivo" v-model="motivo" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="estado" class="form-label">Estado de la cita</label>
          <select id="estado" v-model="estado" class="form-select" required>
            <option value="Pendiente">Pendiente</option>
            <option value="Confirmada">Confirmada</option>
            <option value="Cancelada">Cancelada</option>
          </select>
        </div>
        <button type="submit" class="btn btn-primary">Registrar Cita</button>
      </form>
    </div>
  </div>
</template>

<script>
import { addDoc, collection, getDocs, Timestamp } from 'firebase/firestore';
import { db } from '../firebase';

export default {
  data() {
    return {
      pacienteId: '',
      pacientes: [],
      especialistaId: '',
      especialistas: [],
      fechaHora: '',
      motivo: '',
      estado: 'Pendiente',
      mensajeExito: '',
      mensajeError: '',
      pacienteSeleccionado: {},
      especialistaSeleccionado: {}
    };
  },
  async mounted() {
    const pacientesSnapshot = await getDocs(collection(db, 'pacientes'));
    this.pacientes = pacientesSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));

    const especialistasSnapshot = await getDocs(collection(db, 'especialistas'));
    this.especialistas = especialistasSnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
  },
  watch: {
    pacienteId(newId) {
      this.pacienteSeleccionado = this.pacientes.find(p => p.id === newId) || {};
    },
    especialistaId(newId) {
      this.especialistaSeleccionado = this.especialistas.find(e => e.id === newId) || {};
    }
  },
  methods: {
    async registrarCita() {
      try {
        const paciente = this.pacientes.find(p => p.id === this.pacienteId);
        const especialista = this.especialistas.find(e => e.id === this.especialistaId);
        const docRef = await addDoc(collection(db, 'citas'), {
          pacienteId: this.pacienteId,
          nombrePaciente: `${paciente.nombre} ${paciente.apellidoPaterno} ${paciente.apellidoMaterno}`,
          especialistaId: this.especialistaId,
          nombreEspecialista: `${especialista.nombre} ${especialista.apellidoPaterno} ${especialista.apellidoMaterno}`,
          fechaHora: Timestamp.fromDate(new Date(this.fechaHora)),
          motivo: this.motivo,
          estado: this.estado.toLowerCase(),
          fechaRegistro: Timestamp.now()
        });
        console.log("Cita registrada con ID: ", docRef.id);
        this.mensajeExito = 'Cita registrada con éxito!';
        this.mensajeError = '';
        setTimeout(() => {
          this.mensajeExito = '';
        }, 3000);
        this.pacienteId = '';
        this.especialistaId = '';
        this.fechaHora = '';
        this.motivo = '';
        this.estado = 'Pendiente';
        this.$emit('cita-registrada');
      } catch (e) {
        console.error("Error al registrar cita: ", e);
        this.mensajeError = 'Ocurrió un error al registrar la cita.';
        this.mensajeExito = '';
        setTimeout(() => {
          this.mensajeError = '';
        }, 5000);
      }
    }
  }
}
</script>