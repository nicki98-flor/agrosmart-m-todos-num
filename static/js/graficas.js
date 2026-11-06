
document.addEventListener("DOMContentLoaded", () => {
    // Recuperar los datos enviados por Flask desde resultados.html
    const elementoDatos = document.getElementById("datos-ejecuciones");

    if (!elementoDatos) {
        console.error("No se encontró el elemento datos-ejecuciones.");
        return;
    }

    let ejecuciones;

    try {
        ejecuciones = JSON.parse(elementoDatos.textContent);
    } catch (error) {
        console.error("No se pudieron leer los datos de las simulaciones:", error);
        return;
    }

    if (!Array.isArray(ejecuciones) || ejecuciones.length === 0) {
        console.warn("No hay ejecuciones para mostrar.");
        return;
    }

    ejecuciones.forEach((ejecucion, index) => {
        const filas = ejecucion.resultados || [];
        const canvas = document.getElementById(`grafica${index + 1}`);

        if (!canvas || filas.length === 0) {
            console.warn(`No hay datos o canvas para la ejecución ${index + 1}.`);
            return;
        }

        new Chart(canvas, {
            type: "line",

            data: {
                labels: filas.map(fila => fila.tiempo),

                datasets: [
                    {
                        label: "Solución analítica",
                        data: filas.map(fila => fila.analitica),
                        borderColor: "#269B70",
                        backgroundColor: "#269B70",
                        borderWidth: 3,
                        pointRadius: 0,
                        tension: 0.25
                    },
                    {
                        label: "Método de Heun",
                        data: filas.map(fila => fila.heun),
                        borderColor: "#E6A23C",
                        backgroundColor: "#E6A23C",
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.25
                    },
                    {
                        label: "Método RK4",
                        data: filas.map(fila => fila.rk4),
                        borderColor: "#9270C8",
                        backgroundColor: "#9270C8",
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.25
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                plugins: {
                    legend: {
                        position: "bottom"
                    },
                    tooltip: {
                        callbacks: {
                            title: (items) => `Mes ${items[0].label}`,
                            label: (item) =>
                                `${item.dataset.label}: ${Number(item.raw).toFixed(4)} productores`
                        }
                    }
                },

                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Tiempo (meses)"
                        }
                    },

                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: "Productores adoptantes"
                        }
                    }
                }
            }
        });
    });
});
