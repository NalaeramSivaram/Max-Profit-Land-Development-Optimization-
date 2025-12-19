# 🏗️ Max Profit Land Development Optimization

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Algorithm](https://img.shields.io/badge/Algorithm-Optimization-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 📌 Problem Summary

This project solves a **profit maximization problem under time constraints**.

A landowner can construct different types of properties on infinite land, but:
- Only **one property can be built at a time**
- Each property has a fixed **construction time**
- Earnings begin **only after construction is completed**

The objective is to determine the **optimal mix of properties** that maximizes total earnings within a given time limit.

---

## 🏢 Property Specifications

| Property | Build Time (units) | Land Used | Earnings per Time Unit |
|---------|-------------------|-----------|------------------------|
| Theatre (T) | 5 | 2×1 | $1500 |
| Pub (P) | 4 | 1×1 | $1000 |
| Commercial Park (C) | 10 | 3×1 | $2000 |

---

## ⚙️ Constraints

- No parallel construction
- Infinite land availability
- Earnings start only after build completion
- Input: total time units `n`
- Output format:
T:<count> P:<count> C:<count>

---

## 🎯 Objective

Given `n` units of time:
- Choose the number of Theatres, Pubs, and Commercial Parks
- Maximize total earnings
- Return the optimal configuration

---

## 🧠 Program Approach

The solution is based on **evaluating all feasible construction combinations** rather than using a greedy approach.

### Step-by-Step Approach

1. **Iterate through possible counts** of each property type  
 - Theatre, Pub, Commercial Park
2. **Validate construction time**
 - Ensure total build time does not exceed `n`
3. **Calculate operational time**
 - Remaining time after construction
4. **Compute earnings**

---

earnings = operational_time × earning_rate
5. **Track maximum profit**
- Store the configuration yielding highest earnings
6. **Output optimal mix**
- Display counts of T, P, and C

### Why This Works

- Greedy selection fails because high-earning properties take longer to build
- The approach explicitly models **time-to-build vs earning trade-off**
- Limited property types keep the search space manageable

---

## 🧪 Sample Test Cases

### Test Case 1

Input:
Time Unit: 7

Output:
T:1 P:0 C:0
Earnings: $3000

---

## 📊 Why These Results Are Optimal

- Higher earning properties may delay revenue due to longer construction time
- Faster construction enables earlier operational earnings
- The algorithm balances **build time vs earning rate**

---

## ⏱️ Complexity Analysis

- **Time Complexity:** O(n²)
- **Space Complexity:** O(1)

Efficient due to a small and bounded search space.

---

## 🚧 Challenges & Fixes

| Issue | Resolution |
|-----|------------|
Greedy strategy failed | Evaluated all feasible combinations |
Incorrect profit calculation | Separated build time and earning time |
Edge cases for small `n` | Added feasibility checks |
Delayed revenue from large builds | Accounted operational duration |

---

## 🧠 Key Learnings

- Greedy algorithms can fail under time constraints
- Trade-off analysis is essential for real-world optimization
- Correct modeling leads to optimal decisions

---

## ▶️ How to Run

```bash
python Max_Profit.py
