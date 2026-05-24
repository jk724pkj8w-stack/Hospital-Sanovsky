<template>
  <div class="container mt-5">
    <h2 class="text-center">Bienvenido al Hospital Sanovsky</h2>

    <div class="row mt-4">
      <div class="col-12 col-md-4 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Registrar Paciente</h5>
            <p class="card-text">Añade un nuevo paciente al sistema.</p>
            <router-link to="/registro-paciente" class="btn btn-primary">Registrar</router-link>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Registrar Especialista</h5>
            <p class="card-text">Añade un nuevo especialista al sistema.</p>
            <router-link to="/registro-especialista" class="btn btn-primary">Registrar</router-link>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-4 mb-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Agendar Cita</h5>
            <p class="card-text">Agenda una cita médica para un paciente.</p>
            <router-link to="/agendar-cita" class="btn btn-primary">Agendar</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useRouter } from 'vue-router';

const router = useRouter();
const auth = getAuth();
const isAuthenticated = ref(false);

onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log('Usuario autenticado:', user);
      isAuthenticated.value = true;
    } else {
      console.log('Usuario no autenticado');
      isAuthenticated.value = false;
      router.push('/login');
    }
  });
});
</script>

<style scoped>
.container {
  max-width: 1200px;
}

.card {
  border-radius: 10px;
}
</style>