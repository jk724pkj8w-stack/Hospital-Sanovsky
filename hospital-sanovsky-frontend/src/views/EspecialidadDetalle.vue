<script>
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: 'EspecialidadDetalle',
  setup() {
    const route = useRoute();
    const especialidad = ref(null);
    const loading = ref(true);
    const error = ref('');

    const fetchEspecialidad = async () => {
      try {
        const id = route.params.id;
        const response = await axios.get(`http://192.168.17.2:7777/especialidadDetalle/${id}`);
        especialidad.value = response.data;
        console.log("Especialidad cargada:", response.data);
      } catch (err) {
        error.value = 'No se pudo cargar la especialidad.';
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchEspecialidad);

    return {
      especialidad,
      loading,
      error
    };
  }
};
</script>

<template>
  <div class="container my-5 d-flex justify-content-center">
    <div v-if="loading" class="text-center w-100">
      <p>Cargando especialidad...</p>
    </div>

    <div v-if="error" class="alert alert-danger w-100 text-center">
      {{ error }}
    </div>

    <div v-if="especialidad" class="card shadow-lg p-4" style="max-width: 600px; width: 100%;">
      <div class="card-body">
        <h2 class="card-title text-center text-primary mb-4">
          <i class="bi bi-clipboard2-heart me-2"></i>{{ especialidad.nombre || 'Nombre no disponible' }}
        </h2>

        <p class="card-text fs-5">
          {{ especialidad.descripcion || 'Descripción no disponible' }}
        </p>

        <div class="mt-4">
          <h6 class="text-muted">
            <i class="bi bi-hospital"></i> Área Médica:
          </h6>
          <p class="mb-0">{{ especialidad.area || 'Área no especificada' }}</p>
        </div>
      </div>

      <div class="text-center mt-4">
        <router-link to="/especialidades" class="btn btn-outline-secondary">
          <i class="bi bi-arrow-left-circle me-2"></i>
          Volver a Especialidades
        </router-link>
      </div>
    </div>
  </div>
</template>