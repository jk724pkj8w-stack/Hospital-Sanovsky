<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">¡Hola, {{ userName }}! Hoy es un buen día para salvar vidas</h2>

    <div class="row mt-4">
      <!-- Card for Register Patient -->
      <div class="col-12 col-md-4 mb-4">
        <div class="card shadow-sm rounded">
          <div class="card-body d-flex flex-column align-items-center">
            <i class="fas fa-user-plus fa-3x mb-3"></i>
            <h5 class="card-title">Registrar Paciente</h5>
            <p class="card-text text-center">Añade un nuevo paciente al sistema.</p>
            <router-link to="/registro-paciente" class="btn btn-primary w-100">Registrar</router-link>
          </div>
        </div>
      </div>

      <!-- Card for Register Specialist -->
      <div class="col-12 col-md-4 mb-4">
        <div class="card shadow-sm rounded">
          <div class="card-body d-flex flex-column align-items-center">
            <i class="fas fa-stethoscope fa-3x mb-3"></i>
            <h5 class="card-title">Registrar Especialista</h5>
            <p class="card-text text-center">Añade un nuevo especialista al sistema.</p>
            <router-link to="/registro-especialista" class="btn btn-primary w-100">Registrar</router-link>
          </div>
        </div>
      </div>

      <!-- Card for Schedule Appointment -->
      <div class="col-12 col-md-4 mb-4">
        <div class="card shadow-sm rounded">
          <div class="card-body d-flex flex-column align-items-center">
            <i class="fas fa-calendar-check fa-3x mb-3"></i>
            <h5 class="card-title">Agendar Cita</h5>
            <p class="card-text text-center">Agenda una cita médica para un paciente.</p>
            <router-link to="/agendar-cita" class="btn btn-primary w-100 mb-2">Agendar</router-link>
            <router-link to="/ver-citas" class="btn btn-primary w-100">Ver Citas</router-link>
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
const userName = ref('');

onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      isAuthenticated.value = true;
      userName.value = user.displayName || 'Usuario';
    } else {
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
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-body {
  text-align: center;
}

.fas {
  color: #007bff;
  font-size: 3rem;
}

.card-body h5 {
  font-size: 1.25rem;
  font-weight: bold;
}

.card-body p {
  font-size: 1rem;
  margin-bottom: 20px;
}

.btn {
  border-radius: 25px;
  font-size: 1rem;
}

.text-center h2 {
  color: #007bff;
  font-weight: 600;
}

.row {
  margin-top: 40px;
}

@media (max-width: 768px) {
  .card {
    margin-bottom: 20px;
  }
}
</style>