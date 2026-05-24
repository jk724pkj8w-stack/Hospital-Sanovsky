<template>
    <div class="container mt-5">
      <h2 class="text-center">Especialidades Disponibles</h2>
      <div class="row">
        <div class="col-12 col-md-4" v-for="especialidad in especialidades" :key="especialidad.id">
          <div class="card">
            <div class="text-center my-3" v-html="especialidad.icono"></div>
            <div class="card-body">
              <h5 class="card-title">{{ especialidad.nombre }}</h5>
              <p class="card-text">{{ especialidad.descripcion }}</p>
              <router-link :to="`/especialidades/${especialidad.id}`" class="btn btn-primary">Ver más</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Especialidades',
    data() {
      return {
        especialidades: [
          {
            id: '1',
            nombre: 'Cardiología',
            descripcion: 'Especialidad en el corazón y el sistema circulatorio.',
            icono: '<i class="bi bi-heart-pulse-fill fs-1 text-danger"></i>'
          },
          {
            id: '3',
            nombre: 'Neurología',
            descripcion: 'Especialidad en el cerebro y el sistema nervioso.',
            icono: '<i class="bi bi-puzzle-fill fs-1 text-info"></i>'
          },
          {
            id: '2',
            nombre: 'Pediatría',
            descripcion: 'Especialidad en la atención médica infantil.',
            icono: '<i class="bi bi-emoji-smile fs-1 text-warning"></i>'
          }
        ]
      };
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
  }
  .card {
    margin-bottom: 30px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  }
  .card .text-center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
  }
  .card-title {
    font-weight: 600;
    font-size: 1.25rem;
    text-align: center;
  }
  .card-text {
    text-align: center;
    min-height: 60px;
  }
  .btn {
    display: block;
    margin: 0 auto;
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

  .card {
    animation: fade-in 0.6s ease-in-out;
  }
  </style>