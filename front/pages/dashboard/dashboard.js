/* ===================================
   Distributor Dashboard - Real Data (MODIFIED FOR DEMO MODE)
   =================================== */

'use strict';

document.addEventListener('DOMContentLoaded', async () => {
    // --- AUTHENTICATION AND ROLE CHECKS TEMPORARILY DISABLED FOR DEMO ---
    
    // Check authentication (DISABLED)
    // if (!api.isAuthenticated()) {
    //     window.location.href = '/front/pages/account/account.html';
    //     return;
    // }

    // Check if user is distributor (DISABLED)
    // if (!api.isDistributor()) {
    //     alert('Access denied. Distributor account required.');
    //     window.location.href = '/front/pages/customer/customer.html';
    //     return;
    // }

    // Load dashboard data (This now sets a generic title, skipping user data fetch)
    await loadDashboardData();
    
    // Initialize charts with existing mock data
    initializeCharts();
});

async function loadDashboardData() {
    // --- MODIFIED TO BYPASS API CALL FOR USER NAME ---
    
    const welcomeHeader = document.querySelector('.dashboard-header h1');
    
    // Update welcome message to a generic title 
    if (welcomeHeader) {
        welcomeHeader.textContent = `Medical Distributors Dashboard (Demo Mode)`;
    }

    /*
    // ORIGINAL LOGIC (COMMENTED OUT TO PREVENT FAILURE WITHOUT A VALID TOKEN)
    try {
        // Get current user data (this would fail without a token)
        const user = await api.getCurrentUser();
        
        // Update welcome message
        if (welcomeHeader && user.full_name) {
            welcomeHeader.textContent = `${user.full_name}'s Dashboard`;
        }
    } catch (error) {
        // Suppress or log the error, but do not redirect
        console.warn('Authentication check bypassed. Could not fetch user data.');
    }
    */
}

function initializeCharts() {
    // Common chart options
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        layout: { 
            padding: { top: 5, bottom: 40, left: 25, right: 10 } 
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#343a40',
                    font: { family: 'Montserrat', size: 14, weight: '600' },
                    boxWidth: 18,
                    boxHeight: 10
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.8)',
                titleFont: { size: 13, weight: 'bold', family: 'Montserrat' },
                bodyFont: { size: 12, family: 'Montserrat' },
                padding: 10,
                cornerRadius: 8
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    color: '#343a40',
                    font: { family: 'Montserrat', size: 13, weight: '600' },
                    padding: 5
                },
                grid: { display: false }
            },
            x: {
                ticks: {
                    color: '#343a40',
                    font: { family: 'Montserrat', size: 14, weight: '700' },
                    padding: 10
                },
                grid: { display: false }
            }
        }
    };

    // Revenue Trends Chart
    const revenueCtx = document.getElementById('revenueTrendsChart')?.getContext('2d');
    if (revenueCtx) {
        const gradient = revenueCtx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(0, 86, 179, 0.3)');
        gradient.addColorStop(1, 'rgba(0, 86, 179, 0)');

        new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: ['Oct 1', 'Oct 2', 'Oct 3', 'Oct 4', 'Oct 5', 'Oct 6', 'Oct 7'],
                datasets: [
                    {
                        label: 'Daily Revenue (IQD)',
                        data: [18602000, 20239500, 20946200, 18078000, 20914500, 19372500, 22401000],
                        borderColor: '#0056b3',
                        backgroundColor: gradient,
                        borderWidth: 2.5,
                        pointRadius: 3,
                        pointBackgroundColor: '#0056b3',
                        tension: 0.35,
                        fill: true
                    },
                    {
                        label: 'Online Contribution (IQD)',
                        data: [7336000, 8253000, 8777000, 6681000, 8777000, 7598000, 9301000],
                        borderColor: '#28a745',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointBackgroundColor: '#28a745',
                        tension: 0.35
                    }
                ]
            },
            options: chartOptions
        });
    }

    // Refund Analysis Chart
    const refundCtx = document.getElementById('refundAnalysisChart')?.getContext('2d');
    if (refundCtx) {
        new Chart(refundCtx, {
            type: 'bar',
            data: {
                labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                datasets: [
                    {
                        label: 'Total Orders',
                        data: [150, 180, 140, 120, 170, 200, 160],
                        backgroundColor: 'rgba(0, 86, 179, 0.8)',
                        borderRadius: 6
                    },
                    {
                        label: 'Daily Refunds',
                        data: [4, 6, 3, 5, 4, 7, 5],
                        backgroundColor: 'rgba(220, 53, 69, 0.8)',
                        borderRadius: 6
                    }
                ]
            },
            options: chartOptions
        });
    }

    // Payment Methods Chart
    const paymentCtx = document.getElementById('paymentMethodsChart')?.getContext('2d');
    if (paymentCtx) {
        new Chart(paymentCtx, {
            type: 'doughnut',
            data: {
                labels: ['Zain Cash', 'Asia Hawala', 'Cash on Delivery (COD)', 'Bank Card / Other'],
                datasets: [{
                    data: [40, 30, 15, 15],
                    backgroundColor: ['#0056b3', '#28a745', '#dc3545', '#ffc107'],
                    borderWidth: 3
                }]
            },
            options: {
                maintainAspectRatio: false,
                cutout: '73%',
                layout: { padding: { top: 0, bottom: 60 } },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#343a40',
                            font: { family: 'Montserrat', size: 13, weight: '600' },
                            padding: 18,
                            boxWidth: 18
                        }
                    }
                }
            }
        });
    }

    // Hourly Orders Chart
    const hourlyCtx = document.getElementById('hourlyOrdersChart')?.getContext('2d');
    if (hourlyCtx) {
        new Chart(hourlyCtx, {
            type: 'bar',
            data: {
                labels: ['8-10 AM', '10-12 PM', '12-2 PM', '2-4 PM', '4-6 PM', '6-8 PM'],
                datasets: [{
                    label: 'Orders Count',
                    data: [40, 65, 90, 85, 55, 35],
                    backgroundColor: 'rgba(40, 167, 69, 0.8)',
                    borderRadius: 6
                }]
            },
            options: chartOptions
        });
    }
}
// /* ===================================
//    Distributor Dashboard - Real Data
//    =================================== */

// 'use strict';

// document.addEventListener('DOMContentLoaded', async () => {
//     // Check authentication
//     if (!api.isAuthenticated()) {
//         // Redirect to login/account page if not authenticated
//         window.location.href = '/front/pages/account/account.html';
//         return;
//     }

//     // Check if user is distributor
//     // This requires the user data to be in localStorage or a fresh check
//     const isDistributor = api.isDistributor();
//     if (!isDistributor) {
//         alert('Access denied. Distributor account required.');
//         // Redirect to the customer dashboard if not a distributor
//         window.location.href = '/front/pages/customer/customer.html';
//         return;
//     }

//     // Load dashboard data (User Name)
//     await loadDashboardData();
    
//     // Initialize charts with existing mock data
//     initializeCharts();
// });

// async function loadDashboardData() {
//     try {
//         // Get current user data (also re-validates token on the backend)
//         const user = await api.getCurrentUser();
        
//         // Update welcome message
//         const welcomeHeader = document.querySelector('.dashboard-header h1');
//         if (welcomeHeader && user.full_name) {
//             // Update the header with the user's full name
//             welcomeHeader.textContent = `${user.full_name}'s Dashboard`;
//         }

//         // The KPI cards in the HTML are currently populated with mock data.
//         // The real KPI values (Revenue, Orders, etc.) would typically come
//         // from a dedicated '/dashboard/kpis' endpoint, not '/products'.
//         // For now, we will use the existing mock data and skip the incorrect
//         // calculation based on product inventory.
        
//     } catch (error) {
//         console.error('Error loading dashboard data:', error);
//         // If getCurrentUser fails (e.g., token expired), it clears the token
//         // and throws, leading to a user-friendly alert.
//         alert('Error loading user data. You might be logged out. Please log in again.');
//         window.location.href = '/front/pages/account/account.html'; // Redirect on severe failure
//     }
// }

// // Removed the old 'updateKPIs' function as its logic was incorrect (using products for revenue).
// // The HTML hardcoded values will be used until a proper API endpoint is implemented.

// function initializeCharts() {
//     // Common chart options
//     const chartOptions = {
//         responsive: true,
//         maintainAspectRatio: false,
//         layout: { 
//             padding: { top: 5, bottom: 40, left: 25, right: 10 } 
//         },
//         plugins: {
//             legend: {
//                 position: 'top',
//                 labels: {
//                     color: '#343a40',
//                     font: { family: 'Montserrat', size: 14, weight: '600' },
//                     boxWidth: 18,
//                     boxHeight: 10
//                 }
//             },
//             tooltip: {
//                 backgroundColor: 'rgba(0,0,0,0.8)',
//                 titleFont: { size: 13, weight: 'bold', family: 'Montserrat' },
//                 bodyFont: { size: 12, family: 'Montserrat' },
//                 padding: 10,
//                 cornerRadius: 8
//             }
//         },
//         scales: {
//             y: {
//                 beginAtZero: true,
//                 ticks: {
//                     color: '#343a40',
//                     font: { family: 'Montserrat', size: 13, weight: '600' },
//                     padding: 5
//                 },
//                 grid: { display: false }
//             },
//             x: {
//                 ticks: {
//                     color: '#343a40',
//                     font: { family: 'Montserrat', size: 14, weight: '700' },
//                     padding: 10
//                 },
//                 grid: { display: false }
//             }
//         }
//     };

//     // Revenue Trends Chart
//     const revenueCtx = document.getElementById('revenueTrendsChart')?.getContext('2d');
//     if (revenueCtx) {
//         const gradient = revenueCtx.createLinearGradient(0, 0, 0, 400);
//         gradient.addColorStop(0, 'rgba(0, 86, 179, 0.3)');
//         gradient.addColorStop(1, 'rgba(0, 86, 179, 0)');

//         new Chart(revenueCtx, {
//             type: 'line',
//             data: {
//                 labels: ['Oct 1', 'Oct 2', 'Oct 3', 'Oct 4', 'Oct 5', 'Oct 6', 'Oct 7'],
//                 datasets: [
//                     {
//                         label: 'Daily Revenue (IQD)',
//                         data: [18602000, 20239500, 20946200, 18078000, 20914500, 19372500, 22401000],
//                         borderColor: '#0056b3',
//                         backgroundColor: gradient,
//                         borderWidth: 2.5,
//                         pointRadius: 3,
//                         pointBackgroundColor: '#0056b3',
//                         tension: 0.35,
//                         fill: true
//                     },
//                     {
//                         label: 'Online Contribution (IQD)',
//                         data: [7336000, 8253000, 8777000, 6681000, 8777000, 7598000, 9301000],
//                         borderColor: '#28a745',
//                         borderWidth: 2,
//                         pointRadius: 3,
//                         pointBackgroundColor: '#28a745',
//                         tension: 0.35
//                     }
//                 ]
//             },
//             options: chartOptions
//         });
//     }

//     // Refund Analysis Chart
//     const refundCtx = document.getElementById('refundAnalysisChart')?.getContext('2d');
//     if (refundCtx) {
//         new Chart(refundCtx, {
//             type: 'bar',
//             data: {
//                 labels: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
//                 datasets: [
//                     {
//                         label: 'Total Orders',
//                         data: [150, 180, 140, 120, 170, 200, 160],
//                         backgroundColor: 'rgba(0, 86, 179, 0.8)',
//                         borderRadius: 6
//                     },
//                     {
//                         label: 'Daily Refunds',
//                         data: [4, 6, 3, 5, 4, 7, 5],
//                         backgroundColor: 'rgba(220, 53, 69, 0.8)',
//                         borderRadius: 6
//                     }
//                 ]
//             },
//             options: chartOptions
//         });
//     }

//     // Payment Methods Chart
//     const paymentCtx = document.getElementById('paymentMethodsChart')?.getContext('2d');
//     if (paymentCtx) {
//         new Chart(paymentCtx, {
//             type: 'doughnut',
//             data: {
//                 labels: ['Zain Cash', 'Asia Hawala', 'Cash on Delivery (COD)', 'Bank Card / Other'],
//                 datasets: [{
//                     data: [40, 30, 15, 15],
//                     backgroundColor: ['#0056b3', '#28a745', '#dc3545', '#ffc107'],
//                     borderWidth: 3
//                 }]
//             },
//             options: {
//                 maintainAspectRatio: false,
//                 cutout: '73%',
//                 layout: { padding: { top: 0, bottom: 60 } },
//                 plugins: {
//                     legend: {
//                         position: 'bottom',
//                         labels: {
//                             color: '#343a40',
//                             font: { family: 'Montserrat', size: 13, weight: '600' },
//                             padding: 18,
//                             boxWidth: 18
//                         }
//                     }
//                 }
//             }
//         });
//     }

//     // Hourly Orders Chart
//     const hourlyCtx = document.getElementById('hourlyOrdersChart')?.getContext('2d');
//     if (hourlyCtx) {
//         new Chart(hourlyCtx, {
//             type: 'bar',
//             data: {
//                 labels: ['8-10 AM', '10-12 PM', '12-2 PM', '2-4 PM', '4-6 PM', '6-8 PM'],
//                 datasets: [{
//                     label: 'Orders Count',
//                     data: [40, 65, 90, 85, 55, 35],
//                     backgroundColor: 'rgba(40, 167, 69, 0.8)',
//                     borderRadius: 6
//                 }]
//             },
//             options: chartOptions
//         });
//     }
// }