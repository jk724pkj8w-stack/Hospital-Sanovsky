<template>
  <div class="container">
    <h2 class="text-center my-4">Médicos Disponibles</h2>

    <!-- Mensaje de carga mientras los datos se están recuperando -->
    <div v-if="loading" class="text-center">
      <p>Cargando médicos...</p>
    </div>

    <!-- Si hay un error, muestra un mensaje -->
    <div v-if="error" class="alert alert-danger text-center">
      <p>{{ error }}</p>
    </div>

    <!-- Si hay médicos, muestra las tarjetas -->
    <div v-if="medicos.length > 0" class="row">
      <div class="col-md-4 mb-4" v-for="medico in medicos" :key="medico.id">
        <div class="card h-100 shadow-sm">
          <div class="text-center my-3">
            <i v-if="medico.sexo === 'Masculino'" class="bi bi-person-fill fs-1 text-primary"></i>
            <i v-else-if="medico.sexo === 'Femenino'" class="bi bi-person-fill fs-1 text-danger"></i>
            <i v-else class="bi bi-person-fill fs-1 text-secondary"></i>
          </div>
          <div class="card-body">
            <h5 class="card-title">
              {{ medico.sexo === 'Masculino' ? 'Dr. ' : medico.sexo === 'Femenino' ? 'Dra. ' : '' }}{{ medico.nombre }}
            </h5>
            <p class="card-text"><strong>Especialidad:</strong> {{ medico.especialidad }}</p>
            <p class="card-text"><strong>Teléfono:</strong> {{ medico.telefono }}</p>
            <router-link
              :to="`/agendar-cita?doctor_id=${medico.id}&doctor_nombre=${encodeURIComponent(medico.nombre)}`"
              class="btn btn-primary mt-2 w-100"
            >
              Agendar cita
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Si no hay médicos disponibles -->
    <div v-else class="text-center mt-4">
      <p>No hay médicos disponibles.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      medicos: [],
      loading: true,   // Para controlar el estado de carga
      error: null      // Para almacenar cualquier error
    };
  },
  created() {
    this.fetchMedicos();
  },
  methods: {
    async fetchMedicos() {
      try {
        const response = await axios.get('http://192.168.17.2:7777/medicos');
        this.medicos = response.data;
      } catch (error) {
        console.error('Error al obtener médicos:', error);
        this.error = 'Hubo un error al cargar los médicos. Intenta nuevamente.';
      } finally {
        this.loading = false;  // Termina la carga
      }
    }
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.card {
  border-radius: 10px;
  transition: transform 0.4s ease, box-shadow 0.4s ease;
  animation: fade-in 0.8s ease-out;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1);
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.card-body {
  text-align: center;
}
.card-img-top {
  border-radius: 10px 10px 0 0;
}

.btn-primary {
  font-weight: 500;
  border-radius: 8px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.03);
}
</style>