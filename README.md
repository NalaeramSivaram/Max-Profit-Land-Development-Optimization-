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
