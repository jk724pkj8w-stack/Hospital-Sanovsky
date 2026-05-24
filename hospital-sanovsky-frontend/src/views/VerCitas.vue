<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-center text-primary">Citas Médicas</h2>

    <div v-if="loading" class="text-center">Cargando citas...</div>
    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <table v-if="citas.length > 0" class="table table-striped">
      <thead>
        <tr>
          <th>Paciente</th>
          <th>Especialista</th>
          <th>Fecha</th>
          <th>Motivo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cita in citas" :key="cita.id">
          <td>{{ cita.nombrePaciente }}</td>
          <td>{{ cita.nombreEspecialista }}</td>
          <td>{{ formatearFechaHora(cita.fechaHora) }}</td>
          <td>{{ cita.motivo }}</td>
          <td>
            <button class="btn btn-sm btn-warning me-2" @click="abrirModal(cita)">Editar</button>
            <button class="btn btn-sm btn-danger" @click="cancelarCita(cita.id)">Cancelar</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="text-center">No hay citas registradas.</div>

    <div v-if="mostrandoModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Editar Cita</h5>
            <button type="button" class="btn-close" @click="cerrarModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Fecha</label>
              <input type="date" class="form-control" v-model="nuevaFecha">
            </div>
            <div class="mb-3">
              <label class="form-label">Hora</label>
              <input type="time" class="form-control" v-model="nuevaHora">
            </div>
            <div class="mb-3">
              <label class="form-label">Motivo</label>
              <textarea class="form-control" v-model="nuevoMotivo"></textarea>
            </div>
            <div v-if="errorValidacion" class="alert alert-danger">
              {{ errorValidacion }}
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cerrarModal">Cancelar</button>
            <button class="btn btn-primary" @click="guardarCambios">Guardar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const citas = ref([]);
const loading = ref(true);
const error = ref('');

const citaSeleccionada = ref(null);
const nuevaFecha = ref('');
const nuevaHora = ref('');
const nuevoMotivo = ref('');
const mostrandoModal = ref(false);
const errorValidacion = ref('');

const abrirModal = (cita) => {
  citaSeleccionada.value = cita;
  nuevaFecha.value = cita.fecha;
  nuevaHora.value = cita.hora || '';
  nuevoMotivo.value = cita.motivo;
  mostrandoModal.value = true;
};

const cerrarModal = () => {
  mostrandoModal.value = false;
  errorValidacion.value = '';
};

const guardarCambios = async () => {
  const hoy = new Date().toISOString().split('T')[0];

  if (!nuevaFecha.value || !nuevaHora.value || !nuevoMotivo.value.trim()) {
    errorValidacion.value = 'Por favor completa todos los campos antes de guardar.';
    return;
  }

  if (nuevaFecha.value < hoy) {
    errorValidacion.value = 'La fecha no puede estar en el pasado.';
    return;
  }

  if (!/^\d{2}:\d{2}$/.test(nuevaHora.value)) {
    errorValidacion.value = 'La hora debe tener el formato HH:MM.';
    return;
  }

  if (nuevoMotivo.value.trim().length < 5) {
    errorValidacion.value = 'El motivo debe tener al menos 5 caracteres.';
    return;
  }

  try {
    await axios.put(`http://192.168.17.2:7777/cita/${citaSeleccionada.value.id}`, {
      fecha: nuevaFecha.value,
      hora: nuevaHora.value,
      motivo: nuevoMotivo.value
    }, {
      headers: {
        'x-api-key': 'secret123'
      }
    });

    citaSeleccionada.value.fecha = nuevaFecha.value;
    citaSeleccionada.value.hora = nuevaHora.value;
    citaSeleccionada.value.motivo = nuevoMotivo.value;
    cerrarModal();
  } catch (error) {
    alert('Error al actualizar la cita.');
  }
};

const cancelarCita = async (id) => {
  const confirmar = confirm('¿Estás seguro de que deseas cancelar esta cita?');
  if (!confirmar) return;

  try {
    await axios.delete(`http://192.168.17.2:7777/cita/${id}`, {
      headers: {
        'x-api-key': 'secret123' // Ajusta esto si usas una API Key real
      }
    });
    citas.value = citas.value.filter(cita => cita.id !== id);
  } catch (err) {
    alert('Error al cancelar la cita.');
  }
};

const formatearFechaHora = (fecha) => {
  if (!fecha) return '—';
  const d = new Date(fecha);
  return d.toLocaleDateString() + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
};

onMounted(async () => {
  try {
    const response = await axios.get('http://192.168.17.2:7777/citas');
    citas.value = response.data;
  } catch (err) {
    error.value = 'No se pudieron cargar las citas.';
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.container {
  max-width: 900px;
}
.modal {
  display: block;
}
</style>