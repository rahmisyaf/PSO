import math
import random
import matplotlib.pyplot as plt  # type: ignore

# membuat class Particle dengan parameter posisi x,y dan kecepatan x, y
class Particle :
  def __init__(self, position_x: float, position_y: float, velocity_x: float, velocity_y: float):
    self.position_x = position_x
    self.position_y = position_y
    self.velocity_x = velocity_x
    self.velocity_y = velocity_y
    self.fitness = find_fitness(position_x, position_y)
    self.best_position = (position_x, position_y)

# fungsi objektif yang me-return fitness
def find_fitness(x: float, y: float):
  if -5 <= x <= 5 and -5 <= y <= 5:
    return round(math.sin((3*x + y)*math.pi/180) + (2*x - y)**2 - 2*x + 1.5*y + 2, 3)
  else:
    return float('inf') # kalau melebihi batas yang ditentukan

# fungsi untuk men-generate nilai random float
def generate_random(min_range: int, max_range: int) :
  return round(random.uniform(min_range, max_range), 3)

# fungsi untuk update pbest tiap partikel
def update_particle_best_position(particles):
    for particle in particles :
      particle.fitness = find_fitness(particle.position_x, particle.position_y)

      if particle.fitness < find_fitness(particle.best_position[0], particle.best_position[1]):
            particle.best_position = (particle.position_x, particle.position_y)

# fungsi untuk update gbest
def update_global_best_position(particles, global_best_fitness, global_best_position):
    for particle in particles:
        if particle.fitness < global_best_fitness:
            global_best_fitness = particle.fitness
            global_best_position = (particle.position_x, particle.position_y)

    return global_best_fitness, global_best_position

# fungsi untuk update kecepatan partikel
def update_velocity(inertia_weight, 
                    velocity_x, velocity_y, 
                    c_1, r_1, 
                    particle_best_position, 
                    c_2, r_2, 
                    global_best_position, 
                    particle_position_x, particle_position_y):
  
  new_x_velocity = inertia_weight*velocity_x + c_1*r_1*(particle_best_position[0] - particle_position_x) + c_2*r_2*(global_best_position[0] - particle_position_x)
  new_y_velocity = inertia_weight*velocity_y + c_1*r_1*(particle_best_position[1] - particle_position_y) + c_2*r_2*(global_best_position[1] - particle_position_y)

  return new_x_velocity, new_y_velocity

# fungsi untuk update posisi x dan y
def update_position(particle, min_range, max_range):
    particle.position_x += particle.velocity_x
    particle.position_y += particle.velocity_y

    # validasi domain
    particle.position_x = max(min(particle.position_x, max_range), min_range)
    particle.position_y = max(min(particle.position_y, max_range), min_range)

# fungsi pso yang menerima parameter banyak iterasi, banyak partikel, minimum range, dan maksimum range
def pso(iterations, particles_count, min_range, max_range):
  #inisialisasi kecepatan awal x
  initial_velocity_x: float = 0.0
  #inisialisasi kecepatan awal y
  initial_velocity_y: float = 0.0
  # bobot inersia
  inertia_weight: float = 1.0
  # koefisien akselerasi kognitif
  c_1: float = 1.0
  # koefisien akselerasi sosial
  c_2: float = 0.5

  # array untuk menyimpan nilai (x, y)
  # particles_position= [(1,1), (-1, 1), (2,1)]
  particles_position= []
  particles_length = particles_count

  # men-generate posisi random untuk tiap partikel
  for i in range (particles_length) :
    x = generate_random(min_range, max_range)
    y = generate_random(min_range, max_range)

    particles_position.append((x, y)) # menambahkan ke dalam array particles_position

  print(particles_position) # cetak untuk memastikan isi array

# pembuatan partikel baru dengan posisi dari array particles_position_x
  particles = []
  for i in range (particles_length) :
    x, y = particles_position[i]
    particles.append(Particle(x, y, initial_velocity_x, initial_velocity_y))


# inisialisasi gbest
  global_best_position = particles[0].best_position
  global_best_fitness = particles[0].fitness

# list yang menyimpan data untuk keperluan visualisasi 
  gbest_fitness = [] # kumpulan perubahan fitness dari gbest
  particle_fitnesses = [] # kumpulan perubahan fitness dari partikel
  positions_of_particles = [] # kumpulan posisi
  pbests = [] # kumpulan pbest
  velocities = [] # kumpulan velocity
  iteration_list = [] # kumpulan iterasi
  
  # mulai iterasi
  for iteration in range (iterations):
    # menandakan iterasi ke-berapa
    print(f"\niterasi ke-{iteration + 1}")
    print("-"*120)

    # tambahin banyak iterasi ke list iterasi
    iteration_list.append(iteration + 1)
    
    # update pbest tiap partikel
    update_particle_best_position(particles)

    global_best_fitness, global_best_position = update_global_best_position(particles, 
                                                                            global_best_fitness, 
                                                                            global_best_position)

    # cetak gbest saat ini
    print(f"gBest : {global_best_position} | gBest fitness : {global_best_fitness}")
    print("-"*120)

    # cetak header untuk hasil tiap iterasi
    print("particle |  position (x, y) | f(x, y) |        pBest      |    (Vx, Vy)")
    print("-"*120)

    # simpan data ke array gbest_fitness, particle fitnesses, positions_of_particles, pbests, velocities, dan iteration_list
    gbest_fitness.append(global_best_fitness)
    particle_fitnesses.append([particle.fitness for particle in particles])
    positions_of_particles.append([(particle.position_x, particle.position_y) for particle in particles])
    pbests.append([particle.best_position for particle in particles])
    velocities.append([(particle.velocity_x, particle.velocity_y) for particle in particles])
    iteration_list.append(iteration + 1)

    # ini untuk update kecepatan dan posisi
    for i,particle in enumerate (particles):
      # bilangan acak pada pengalaman individu partikel dengan range [0, 1]
      r_1: float = generate_random(0, 1)
      # bilangan acak pada pengalaman kolektif seluruh populasi dengan range [0, 1]
      r_2: float = generate_random(0, 1)
      # r_1: float = 1.0
      # r_2: float = 1.0

      # update kecepatan x dan y yang disimpan ke variabel sementara
      new_x_velocity, new_y_velocity = update_velocity(inertia_weight, 
                                              particle.velocity_x, particle.velocity_y,
                                              c_1, r_1,
                                              particle.best_position,
                                              c_2, r_2,
                                              global_best_position,
                                              particle.position_x, particle.position_y)
      
      # passing hasil update kecepatan dari variabel sementara ke aslinya
      particle.velocity_x = new_x_velocity
      particle.velocity_y = new_y_velocity

      # cetak data hasil iterasi
      print(f"{i+1:8} | ({particle.position_x:6.3f}, {particle.position_y:6.3f}) | {particle.fitness:6.3f}  | ({particle.best_position[0]:.3f}, {particle.best_position[1]:.3f})  | ({particle.velocity_x:6.3f}, {particle.velocity_y:6.3f})")
      
      #update posisi
      update_position(particle, min_range, max_range)

      # update fitness
      particle.fitness = find_fitness(particle.position_x, particle.position_y)

  # cetak gBest final
  print("-"*120)
  print(f"best solution: {global_best_position} | fitness: {global_best_fitness}")
  print("-"*120)

  # plotting
  # Frame 1: gBest Fitness dan Particle Fitness
  fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

  # Subplot 1: Grafik gBest fitness
  ax1.plot(range(iterations), gbest_fitness, marker='o', markersize=3, linewidth=1, label='gBest Fitness')
  ax1.set_title('gBest Fitness per Iteration')
  ax1.set_xlabel('Iteration')
  ax1.set_ylabel('Fitness')
  ax1.legend(loc='upper right', fontsize=6)
  ax1.grid()

  # Subplot 2: Grafik fitness tiap partikel
  for i in range(particles_count):
    particle_fitnesses_over_iterations = [fitness[i] for fitness in particle_fitnesses]
    ax2.plot(range(iterations), particle_fitnesses_over_iterations, marker='o', markersize=3, linewidth=1, label=f'Particle {i+1} Fitness')
  ax2.set_title('Particle Fitness per Iteration')
  ax2.set_xlabel('Iteration')
  ax2.set_ylabel('Fitness')
  ax2.legend(loc='upper right', fontsize=6)
  ax2.grid()

  plt.tight_layout()
  plt.show()

  # Frame 2: Posisi X dan Y Partikel
  fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(12, 8))

  # Subplot 1: Grafik posisi X partikel
  for i in range(particles_count):
    particle_positions_x = [positions_of_particles[j][i][0] for j in range(iterations)]
    ax3.plot(range(iterations), particle_positions_x, marker='o', markersize=3, linewidth=1, label=f'Particle {i+1} X')
  ax3.set_title('Particle Positions (X)')
  ax3.set_xlabel('Iteration')
  ax3.set_ylabel('X Position')
  ax3.legend(loc='upper right', fontsize=4)
  ax3.grid()

  # Subplot 2: Grafik posisi Y partikel
  for i in range(particles_count):
    particle_positions_y = [positions_of_particles[j][i][1] for j in range(iterations)]
    ax4.plot(range(iterations), particle_positions_y, marker='x', markersize=3, linewidth=1, label=f'Particle {i+1} Y')
  ax4.set_title('Particle Positions (Y)')
  ax4.set_xlabel('Iteration')
  ax4.set_ylabel('Y Position')
  ax4.legend(loc='upper right', fontsize=4)
  ax4.grid()

  plt.tight_layout()
  plt.show()

  # Frame 3: pBest X dan pBest Y
  fig3, (ax5, ax6) = plt.subplots(2, 1, figsize=(12, 8))

  # Subplot 1: Grafik pBest X partikel
  for i in range(particles_count):
    particle_pbests_x = [pbests[j][i][0] for j in range(iterations)]
    ax5.plot(range(iterations), particle_pbests_x, marker='o', markersize=2, linewidth=0.7, label=f'Particle {i+1} pBest (X)')
  ax5.set_title('Particle pBest (X)')
  ax5.set_xlabel('Iteration')
  ax5.set_ylabel('pBest X Position')
  ax5.legend(loc='upper right', fontsize=6)
  ax5.grid()

  # Subplot 2: Grafik pBest Y partikel
  for i in range(particles_count):
    particle_pbests_y = [pbests[j][i][1] for j in range(iterations)]
    ax6.plot(range(iterations), particle_pbests_y, marker='o', markersize=2, linewidth=0.7, label=f'Particle {i+1} pBest (Y)')
  ax6.set_title('Particle pBest (Y)')
  ax6.set_xlabel('Iteration')
  ax6.set_ylabel('pBest Y Position')
  ax6.legend(loc='upper right', fontsize=6)
  ax6.grid()

  plt.tight_layout()
  plt.show()

  # Frame 4: Velocity X dan Velocity Y
  fig4, (ax7, ax8) = plt.subplots(2, 1, figsize=(12, 8))

  # Subplot 1: Grafik velocity X partikel
  for i in range(particles_count):
    particle_velocities_x = [velocities[j][i][0] for j in range(iterations)]
    ax7.plot(range(iterations), particle_velocities_x, marker='o', markersize=2, linewidth=0.7, label=f'Particle {i+1} Velocity (X)')
  ax7.set_title('Particle Velocity (X)')
  ax7.set_xlabel('Iteration')
  ax7.set_ylabel('Velocity X')
  ax7.legend(loc='lower left', fontsize=4)
  ax7.grid()

  # Subplot 2: Grafik velocity Y partikel
  for i in range(particles_count):
    particle_velocities_y = [velocities[j][i][1] for j in range(iterations)]
    ax8.plot(range(iterations), particle_velocities_y, marker='x', markersize=2, linewidth=0.7, label=f'Particle {i+1} Velocity (Y)')
  ax8.set_title('Particle Velocity (Y)')
  ax8.set_xlabel('Iteration')
  ax8.set_ylabel('Velocity Y')
  ax8.legend(loc='upper right', fontsize=4)
  ax8.grid()

  plt.tight_layout()
  plt.show()

# memulai pso
pso(iterations=20, particles_count=10, min_range=-5, max_range=5)
