# 🖐️ Roomates AI

---

## 📄 Public Disclosure of *Hand Gesture Light Control*

**Project by:** Vampire Studios  
**Publication Date:** 29‑11‑2025

---

## 1. Purpose of Disclosure

This document is published as a **public technical disclosure** to establish **prior art**. The intent is to openly disclose the concepts, workflows, and implementation details described herein so that **no exclusive patent rights** may be claimed by any individual or organization over the disclosed ideas, methods, or systems.

---

## 2. Overview of the App Concept

**Hand Gesture Light Control** is an assistive technology project designed to enable users—particularly individuals with physical disabilities—to control electronic appliances using simple hand gestures.

### 🔹 Problem Addressed

Many people around the world face physical challenges that make operating switches or appliances difficult. This project provides a **touch‑free, gesture‑based control system** that allows users to operate electronic devices easily.

> Currently, the system demonstrates **light control**, but the Arduino logic can be extended to control **any electronic appliance**.

### 🔹 Core Idea

This project consists of **two applications**:

* A **Windows application**
* An **Android application**

The system integrates the following components:

* Arduino microcontroller
* HC‑05 Bluetooth module
* Computer vision–based hand gesture recognition using MediaPipe

Recognized hand gestures are processed and converted into control signals, which are then transmitted to the Arduino via Bluetooth for appliance control.

### 🔹 Target Users

* Individuals with physical disabilities
* Users interested in hands‑free or smart‑home control systems

The application runs on **standard consumer devices**, such as Android smartphones and Windows PCs.

---

## 3. System Architecture

The system is composed of the following layers:

### 🔹 Frontend Module

* User interface built using standard UI frameworks
* Displays camera preview and system status
* Captures user interaction implicitly through gestures

### 🔹 Processing / Logic Layer

* Performs real‑time hand detection and gesture recognition
* Applies rule‑based logic to map gestures to actions
* Handles validation, filtering, and gesture stability

### 🔹 Hardware Control Layer

* Encodes gesture results into byte‑level commands
* Transmits commands to Arduino via Bluetooth
* Arduino executes actions (e.g., switching lights ON/OFF)

---

## 4. Core Workflow (Technical Detail)

The system follows the workflow below:

1. User displays a predefined hand gesture (e.g., index finger, two fingers)
2. Camera captures the hand image stream
3. MediaPipe processes landmarks and recognizes the gesture
4. The gesture is mapped to a predefined command
5. The command is sent as byte data to the Arduino
6. Arduino triggers the corresponding appliance control action

This workflow is **deterministic, repeatable**, and hardware‑agnostic.

---

## 5. Key Algorithm / Method (Disclosure)

The central method includes:

* Real‑time input acquisition via camera
* Landmark‑based hand gesture recognition
* Rule‑based gesture classification
* Conditional handling of invalid or unstable gestures
* Output generation as hardware control signals

This method can be implemented using **any general‑purpose programming language** and standard computing hardware.

---

## 6. Variations and Alternative Implementations

The disclosed system may be adapted or re‑implemented using:

* Web or desktop platforms
* Alternative computer‑vision or ML frameworks
* Different programming languages
* Local or cloud‑based processing pipelines
* Other communication protocols (Wi‑Fi, BLE, etc.)

All such variations are considered part of this public disclosure.

---

## 7. Publication Intent

This disclosure is intentionally made **public and unrestricted**. Its publication establishes **prior art under international patent systems** and is intended to prevent any future patent filings that attempt to claim exclusive rights over the disclosed concepts, workflows, or methods.

---

## 8. Licensing

All accompanying source code is released under the **Apache License 2.0**, which includes an **express patent license and patent protection provisions**.

---

### ✅ End of Public Disclosure
