// const voiceEntryBtn = document.getElementById('voiceEntryBtn');
// const transactionModal = document.getElementById('transactionModal');
// const editAmount = document.getElementById('editAmount');
// const editCategory = document.getElementById('editCategory');
// const editType = document.getElementById('editType');
// const saveTransactionBtn = document.getElementById('saveTransaction');
// const cancelTransactionBtn = document.getElementById('cancelTransaction');

// if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
//     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//     const recognition = new SpeechRecognition();

//     recognition.continuous = false;
//     recognition.lang = 'en-US';
//     recognition.interimResults = false;
//     recognition.maxAlternatives = 1;

//     if (voiceEntryBtn) {
//         voiceEntryBtn.addEventListener('click', () => {
//             recognition.start();
//             alert("Listening... Speak your transaction details.");
//         });
//     }

//     recognition.onresult = async (event) => {
//         const voiceText = event.results[0][0].transcript;
//         console.log("Voice Input:", voiceText);

//         if (voiceEntryBtn) {
//             voiceEntryBtn.textContent = "Processing...";
//             voiceEntryBtn.disabled = true;
//         }

//         const response = await fetch('/api/process-voice/', {
//             method: 'POST',
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify({ voice_text: voiceText })
//         });

//         if (voiceEntryBtn) {
//             voiceEntryBtn.textContent = "Voice Entry";
//             voiceEntryBtn.disabled = false;
//         }

//         const data = await response.json();

//         if (data.error) {
//             alert("Error processing voice input.");
//             return;
//         }

//         if (editAmount) editAmount.value = data.amount;
//         if (editCategory) editCategory.value = data.category;
//         if (editType) editType.value = data.transaction_type;

//         if (transactionModal) transactionModal.classList.remove('hidden');
//     };

//     recognition.onerror = (event) => {
//         alert("Voice recognition error: " + event.error);
//     };
// }

// if (saveTransactionBtn) {
//     saveTransactionBtn.addEventListener('click', async () => {
//         const transactionData = {
//             amount: parseFloat(editAmount?.value || 0),
//             transaction_type: editType?.value || 'expense',
//             category: editCategory?.value || ''
//         };

//         const response = await fetch('/api/confirm-transaction/', {
//             method: 'POST',
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(transactionData)
//         });

//         const result = await response.json();

//         if (result.message) {
//             alert("Transaction saved successfully!");
//             if (transactionModal) transactionModal.classList.add('hidden');
//         } else {
//             alert("Error saving transaction.");
//         }
//     });
// }

// if (cancelTransactionBtn) {
//     cancelTransactionBtn.addEventListener('click', () => {
//         if (transactionModal) transactionModal.classList.add('hidden');
//     });
// }

// // Fetch User Data from API
// async function fetchUserProfile() {
//     try {
//         const response = await fetch('/api/user-profile/');
//         const data = await response.json();
//         const userAvatar = document.getElementById('userAvatar');
//         const userName = document.getElementById('userName');
//         const currentDate = document.getElementById('currentDate');
        
//         if (userAvatar) userAvatar.src = data.avatar || 'https://via.placeholder.com/40';
//         if (userName) userName.textContent = data.username || 'User';
//         if (currentDate) {
//             currentDate.textContent = new Date().toLocaleDateString('en-US', { 
//                 weekday: 'long', 
//                 month: 'long', 
//                 day: 'numeric', 
//                 year: 'numeric' 
//             });
//         }
//     } catch (error) {
//         console.error('Error fetching user profile:', error);
//     }
// }

// // Toggle User Dropdown Menu
// const userDropdownBtn = document.getElementById('userDropdownBtn');
// const userDropdown = document.getElementById('userDropdown');

// if (userDropdownBtn && userDropdown) {
//     userDropdownBtn.addEventListener('click', () => {
//         userDropdown.classList.toggle('hidden');
//     });

//     document.addEventListener('click', (event) => {
//         if (!userDropdownBtn.contains(event.target) && !userDropdown.contains(event.target)) {
//             userDropdown.classList.add('hidden');
//         }
//     });
// }

// // Set Savings Progress Bar Width
// const savingsProgressBar = document.getElementById('savingsProgressBar');
// if (savingsProgressBar) {
//     // Get progress from data attribute or window object
//     const progress = window.savingsProgress || 0;
//     savingsProgressBar.style.width = progress + '%';
// }

// // Load User Data on Page Load
// fetchUserProfile();

// // ============ FIXED CHART SECTION ============
// // Use data from window object (passed from Django template)
// const spendingData = window.spendingData || {
//     dates: [],
//     income: [],
//     expenses: [],
//     expense_categories: [],
//     months: [],
//     monthly_expenses: []
// };

// // Initialize charts if elements exist
// if (document.getElementById('spendingChart')) {
//     const spendingChart = echarts.init(document.getElementById('spendingChart'));
//     const expensePieChart = echarts.init(document.getElementById('expensePieChart'));
//     const expenseBarChart = echarts.init(document.getElementById('expenseBarChart'));

//     function updateCharts(data) {
//         if (!data) return;
        
//         // Line Chart (Income vs. Expenses)
//         if (spendingChart) {
//             spendingChart.setOption({
//                 tooltip: { trigger: 'axis' },
//                 legend: { data: ['Income', 'Expenses'] },
//                 xAxis: { type: 'category', data: data.dates || [] },
//                 yAxis: { type: 'value' },
//                 series: [
//                     { name: 'Income', type: 'line', data: data.income || [], smooth: true },
//                     { name: 'Expenses', type: 'line', data: data.expenses || [], smooth: true }
//                 ]
//             });
//         }

//         // Pie Chart (Category-wise Expense Distribution)
//         if (expensePieChart) {
//             expensePieChart.setOption({
//                 tooltip: { trigger: 'item' },
//                 legend: { bottom: 10, left: 'center' },
//                 series: [{
//                     name: 'Expenses by Category',
//                     type: 'pie',
//                     radius: '50%',
//                     data: (data.expense_categories || []).map(item => ({ 
//                         name: item.category, 
//                         value: item.amount 
//                     }))
//                 }]
//             });
//         }

//         // Bar Chart (Monthly Expenses Breakdown)
//         if (expenseBarChart) {
//             expenseBarChart.setOption({
//                 tooltip: { trigger: 'axis' },
//                 xAxis: { type: 'category', data: data.months || [] },
//                 yAxis: { type: 'value' },
//                 series: [{ 
//                     name: 'Monthly Expenses', 
//                     type: 'bar', 
//                     data: data.monthly_expenses || [] 
//                 }]
//             });
//         }
//     }

//     // Load data on page load
//     updateCharts(spendingData);
// }

// // Resize charts on window resize
// window.addEventListener('resize', () => {
//     if (typeof echarts !== 'undefined') {
//         const charts = ['spendingChart', 'expensePieChart', 'expenseBarChart'];
//         charts.forEach(id => {
//             const chart = echarts.getInstanceByDom(document.getElementById(id));
//             if (chart) chart.resize();
//         });
//     }
// });

// // Fetch transactions
// async function fetchTransactions() {
//     try {
//         const response = await fetch('/api/transactions/');
//         const transactions = await response.json();
//         const transactionList = document.getElementById('transactionList');

//         if (!transactionList) return;

//         transactionList.innerHTML = '';

//         if (!transactions || transactions.length === 0) {
//             transactionList.innerHTML = '<p class="text-gray-500">No transactions found.</p>';
//             return;
//         }

//         transactions.forEach(transaction => {
//             let iconClass = "ri-file-list-line text-gray-600";
//             let bgClass = "bg-gray-100";
//             let amountClass = "text-red-600";

//             const categoryName = (transaction.category_name || '').toLowerCase();

//             if (categoryName === "salary" || categoryName === "income") {
//                 iconClass = "ri-bank-line text-green-600";
//                 bgClass = "bg-green-100";
//                 amountClass = "text-green-600";
//             } else if (categoryName === "food" || categoryName === "restaurant") {
//                 iconClass = "ri-restaurant-line text-orange-600";
//                 bgClass = "bg-orange-100";
//             } else if (categoryName === "transport" || categoryName === "travel") {
//                 iconClass = "ri-car-line text-orange-600";
//                 bgClass = "bg-orange-100";
//             } else if (categoryName === "shopping") {
//                 iconClass = "ri-shopping-bag-line text-blue-600";
//                 bgClass = "bg-blue-100";
//             } else if (categoryName === "entertainment" || categoryName === "movies") {
//                 iconClass = "ri-movie-line text-red-600";
//                 bgClass = "bg-red-100";
//             } else if (categoryName === "bills" || categoryName === "utilities") {
//                 iconClass = "ri-flashlight-line text-yellow-600";
//                 bgClass = "bg-yellow-100";
//             } else if (categoryName === "rent") {
//                 iconClass = "ri-home-line text-teal-600";
//                 bgClass = "bg-teal-100";
//             }

//             const formattedAmount = `₹${parseFloat(transaction.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
//             const sign = transaction.category_type === "income" ? "+" : "-";
//             const date = transaction.date ? new Date(transaction.date).toLocaleDateString() : '';

//             const transactionItem = `
//                 <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
//                     <div class="flex items-center">
//                         <div class="w-10 h-10 ${bgClass} rounded-full flex items-center justify-center mr-4">
//                             <i class="${iconClass}"></i>
//                         </div>
//                         <div>
//                             <p class="font-medium text-gray-900">${transaction.description || 'Transaction'}</p>
//                             <p class="text-sm text-gray-500">${transaction.category_name || 'Other'} - ${date}</p>
//                         </div>
//                     </div>
//                     <p class="font-medium ${amountClass}">${sign}${formattedAmount}</p>
//                 </div>
//             `;

//             transactionList.innerHTML += transactionItem;
//         });

//     } catch (error) {
//         console.error('Error fetching transactions:', error);
//         const transactionList = document.getElementById('transactionList');
//         if (transactionList) {
//             transactionList.innerHTML = '<p class="text-gray-500">Error loading transactions.</p>';
//         }
//     }
// }

// // Fetch transactions on page load
// fetchTransactions();

// // For the other API calls, add error handling
// async function fetchWithErrorHandling(url, elementId, emptyMessage = 'No data available') {
//     try {
//         const response = await fetch(url);
//         const data = await response.json();
//         const element = document.getElementById(elementId);
//         if (!element) return;
        
//         element.innerHTML = '';
        
//         if (!data || data.length === 0) {
//             element.innerHTML = `<p class="text-gray-500">${emptyMessage}</p>`;
//             return;
//         }
        
//         return data;
//     } catch (error) {
//         console.error(`Error fetching ${url}:`, error);
//         const element = document.getElementById(elementId);
//         if (element) {
//             element.innerHTML = '<p class="text-gray-500">Service unavailable</p>';
//         }
//     }
// }

// // Simplified versions of other fetch functions
// async function fetchAIInsights() {
//     const data = await fetchWithErrorHandling('/api/ai-insights/', 'aiInsightsBox', 'No insights available');
//     if (!data) return;
    
//     const insightsBox = document.getElementById('aiInsightsBox');
//     if (!insightsBox) return;
    
//     insightsBox.innerHTML = '';
//     data.forEach(insight => {
//         insightsBox.innerHTML += `
//             <div class="p-4 bg-blue-50 rounded-lg mb-4">
//                 <p class="font-medium text-gray-900 mb-2">${insight.title || 'Insight'}</p>
//                 <p class="text-sm text-gray-600 mb-4">${insight.message || ''}</p>
//             </div>
//         `;
//     });
// }

// fetchAIInsights();

// async function fetchUpcomingBills() {
//     const data = await fetchWithErrorHandling('/api/upcoming-bills/', 'billsList', 'No upcoming bills');
//     if (!data) return;
    
//     const billsList = document.getElementById('billsList');
//     if (!billsList) return;
    
//     billsList.innerHTML = '';
//     data.forEach(bill => {
//         const textColor = (bill.days_remaining || 0) <= 7 ? "text-red-600" : "text-gray-900";
//         const formattedAmount = `₹${(bill.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        
//         billsList.innerHTML += `
//             <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
//                 <div>
//                     <p class="font-medium ${textColor}">${bill.name || 'Bill'}</p>
//                     <p class="text-sm text-gray-500">Due in ${bill.days_remaining || 0} days</p>
//                 </div>
//                 <p class="font-medium ${textColor}">${formattedAmount}</p>
//             </div>
//         `;
//     });
// }

// fetchUpcomingBills();

// // Show/Hide Notifications
// const notificationBtn = document.getElementById('notificationBtn');
// const notificationDropdown = document.getElementById('notificationDropdown');

// if (notificationBtn && notificationDropdown) {
//     notificationBtn.addEventListener('click', () => {
//         notificationDropdown.classList.toggle('hidden');
//     });
// }
const voiceEntryBtn = document.getElementById('voiceEntryBtn');
const transactionModal = document.getElementById('transactionModal');
const editAmount = document.getElementById('editAmount');
const editCategory = document.getElementById('editCategory');
const editType = document.getElementById('editType');
const saveTransactionBtn = document.getElementById('saveTransaction');
const cancelTransactionBtn = document.getElementById('cancelTransaction');

if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    if (voiceEntryBtn) {
        voiceEntryBtn.addEventListener('click', () => {
            recognition.start();
            alert("Listening... Speak your transaction details.");
        });
    }

    recognition.onresult = async (event) => {
        const voiceText = event.results[0][0].transcript;
        console.log("Voice Input:", voiceText);

        if (voiceEntryBtn) {
            voiceEntryBtn.textContent = "Processing...";
            voiceEntryBtn.disabled = true;
        }

        const response = await fetch('/api/process-voice/', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ voice_text: voiceText })
        });

        if (voiceEntryBtn) {
            voiceEntryBtn.textContent = "Voice Entry";
            voiceEntryBtn.disabled = false;
        }

        const data = await response.json();

        if (data.error) {
            alert("Error processing voice input.");
            return;
        }

        if (editAmount) editAmount.value = data.amount;
        if (editCategory) editCategory.value = data.category;
        if (editType) editType.value = data.transaction_type;

        if (transactionModal) transactionModal.classList.remove('hidden');
    };

    recognition.onerror = (event) => {
        alert("Voice recognition error: " + event.error);
    };
}

if (saveTransactionBtn) {
    saveTransactionBtn.addEventListener('click', async () => {
        const transactionData = {
            amount: parseFloat(editAmount?.value || 0),
            transaction_type: editType?.value || 'expense',
            category: editCategory?.value || ''
        };

        const response = await fetch('/api/confirm-transaction/', {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(transactionData)
        });

        const result = await response.json();

        if (result.message) {
            alert("Transaction saved successfully!");
            if (transactionModal) transactionModal.classList.add('hidden');
        } else {
            alert("Error saving transaction.");
        }
    });
}

if (cancelTransactionBtn) {
    cancelTransactionBtn.addEventListener('click', () => {
        if (transactionModal) transactionModal.classList.add('hidden');
    });
}

// Fetch User Data from API
async function fetchUserProfile() {
    try {
        const response = await fetch('/api/user-profile/');
        const data = await response.json();
        const userAvatar = document.getElementById('userAvatar');
        const userName = document.getElementById('userName');
        const currentDate = document.getElementById('currentDate');
        
        if (userAvatar) userAvatar.src = data.avatar || 'https://via.placeholder.com/40';
        if (userName) userName.textContent = data.username || 'User';
        if (currentDate) {
            currentDate.textContent = new Date().toLocaleDateString('en-US', { 
                weekday: 'long', 
                month: 'long', 
                day: 'numeric', 
                year: 'numeric' 
            });
        }
    } catch (error) {
        console.error('Error fetching user profile:', error);
    }
}

// Toggle User Dropdown Menu
const userDropdownBtn = document.getElementById('userDropdownBtn');
const userDropdown = document.getElementById('userDropdown');

if (userDropdownBtn && userDropdown) {
    userDropdownBtn.addEventListener('click', () => {
        userDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (event) => {
        if (!userDropdownBtn.contains(event.target) && !userDropdown.contains(event.target)) {
            userDropdown.classList.add('hidden');
        }
    });
}

// ============ FIXED: Check if element exists before setting style ============
const savingsProgressBar = document.getElementById('savingsProgressBar');
if (savingsProgressBar) {
    // Get progress from data attribute or window object
    const progress = window.savingsProgress || 0;
    savingsProgressBar.style.width = progress + '%';
}

// Load User Data on Page Load
fetchUserProfile();

// Use data from window object (passed from Django template)

// Fetch transactions
async function fetchTransactions() {
    try {
        const response = await fetch('/api/transactions/');
        const transactions = await response.json();
        const transactionList = document.getElementById('transactionList');

        if (!transactionList) return;

        transactionList.innerHTML = '';

        if (!transactions || transactions.length === 0) {
            transactionList.innerHTML = '<p class="text-gray-500">No transactions found.</p>';
            return;
        }

        transactions.forEach(transaction => {
            let iconClass = "ri-file-list-line text-gray-600";
            let bgClass = "bg-gray-100";
            let amountClass = "text-red-600";

            const categoryName = (transaction.category_name || '').toLowerCase();

            if (categoryName === "salary" || categoryName === "income") {
                iconClass = "ri-bank-line text-green-600";
                bgClass = "bg-green-100";
                amountClass = "text-green-600";
            } else if (categoryName === "food" || categoryName === "restaurant") {
                iconClass = "ri-restaurant-line text-orange-600";
                bgClass = "bg-orange-100";
            } else if (categoryName === "transport" || categoryName === "travel") {
                iconClass = "ri-car-line text-orange-600";
                bgClass = "bg-orange-100";
            } else if (categoryName === "shopping") {
                iconClass = "ri-shopping-bag-line text-blue-600";
                bgClass = "bg-blue-100";
            } else if (categoryName === "entertainment" || categoryName === "movies") {
                iconClass = "ri-movie-line text-red-600";
                bgClass = "bg-red-100";
            } else if (categoryName === "bills" || categoryName === "utilities") {
                iconClass = "ri-flashlight-line text-yellow-600";
                bgClass = "bg-yellow-100";
            } else if (categoryName === "rent") {
                iconClass = "ri-home-line text-teal-600";
                bgClass = "bg-teal-100";
            }

            const formattedAmount = `₹${parseFloat(transaction.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
            const sign = transaction.category_type === "income" ? "+" : "-";
            const date = transaction.date ? new Date(transaction.date).toLocaleDateString() : '';

            const transactionItem = `
                <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div class="flex items-center">
                        <div class="w-10 h-10 ${bgClass} rounded-full flex items-center justify-center mr-4">
                            <i class="${iconClass}"></i>
                        </div>
                        <div>
                            <p class="font-medium text-gray-900">${transaction.description || 'Transaction'}</p>
                            <p class="text-sm text-gray-500">${transaction.category_name || 'Other'} - ${date}</p>
                        </div>
                    </div>
                    <p class="font-medium ${amountClass}">${sign}${formattedAmount}</p>
                </div>
            `;

            transactionList.innerHTML += transactionItem;
        });

    } catch (error) {
        console.error('Error fetching transactions:', error);
        const transactionList = document.getElementById('transactionList');
        if (transactionList) {
            transactionList.innerHTML = '<p class="text-gray-500">Error loading transactions.</p>';
        }
    }
}

// Fetch transactions on page load
fetchTransactions();

async function fetchWithErrorHandling(url, elementId, emptyMessage = 'No data available') {
    try {
        const response = await fetch(url);
        const data = await response.json();
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.innerHTML = '';
        
        if (!data || data.length === 0) {
            element.innerHTML = `<p class="text-gray-500">${emptyMessage}</p>`;
            return;
        }
        
        return data;
    } catch (error) {
        console.error(`Error fetching ${url}:`, error);
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = '<p class="text-gray-500">Service unavailable</p>';
        }
    }
}

async function fetchAIInsights() {
    const data = await fetchWithErrorHandling('/api/ai-insights/', 'aiInsightsBox', 'No insights available');
    if (!data) return;
    
    const insightsBox = document.getElementById('aiInsightsBox');
    if (!insightsBox) return;
    
    insightsBox.innerHTML = '';
    data.forEach(insight => {
        insightsBox.innerHTML += `
            <div class="p-4 bg-blue-50 rounded-lg mb-4">
                <p class="font-medium text-gray-900 mb-2">${insight.title || 'Insight'}</p>
                <p class="text-sm text-gray-600 mb-4">${insight.message || ''}</p>
            </div>
        `;
    });
}

fetchAIInsights();

async function fetchUpcomingBills() {
    const data = await fetchWithErrorHandling('/api/upcoming-bills/', 'billsList', 'No upcoming bills');
    if (!data) return;
    
    const billsList = document.getElementById('billsList');
    if (!billsList) return;
    
    billsList.innerHTML = '';
    data.forEach(bill => {
        const textColor = (bill.days_remaining || 0) <= 7 ? "text-red-600" : "text-gray-900";
        const formattedAmount = `₹${(bill.amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
        
        billsList.innerHTML += `
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                    <p class="font-medium ${textColor}">${bill.name || 'Bill'}</p>
                    <p class="text-sm text-gray-500">Due in ${bill.days_remaining || 0} days</p>
                </div>
                <p class="font-medium ${textColor}">${formattedAmount}</p>
            </div>
        `;
    });
}

fetchUpcomingBills();

// Show/Hide Notifications
const notificationBtn = document.getElementById('notificationBtn');
const notificationDropdown = document.getElementById('notificationDropdown');

if (notificationBtn && notificationDropdown) {
    notificationBtn.addEventListener('click', () => {
        notificationDropdown.classList.toggle('hidden');
    });
}