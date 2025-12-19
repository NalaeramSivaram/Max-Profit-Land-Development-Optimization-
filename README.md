### 🏗️ Max Profit Land Development Optimization ###

# 📌 Problem Summary

This project solves a profit maximization problem under time constraints.

A landowner can construct different types of properties on infinite land, but:

 Only one property can be built at a time

 Each property has a fixed construction time

Earnings begin only after construction is completed

The objective is to determine the optimal mix of properties that maximizes total earnings within a given time limit.

🏢 Property Specifications
Property	Build Time	Land Used	Earnings / Time Unit
Theatre (T)	5 units	2×1	$1500
Pub (P)	4 units	1×1	$1000
Commercial Park (C)	10 units	3×1	$2000
⚙️ Constraints

No parallel construction

Infinite land availability

Earnings start after build completion

Input: total time units n

Output format:

T:<count> P:<count> C:<count>

🎯 Objective

Given n units of time:

Choose the number of Theatres, Pubs, and Commercial Parks

Maximize total earnings

Return the optimal configuration

🧠 Solution Approach

Brute greedy selection fails due to construction delays

The algorithm evaluates all feasible combinations

For each combination:

Validates total build time ≤ n

Computes operational earnings

Tracks and returns the maximum-profit configuration

This ensures correctness over naive greedy heuristics.
