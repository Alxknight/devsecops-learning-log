# Security Audit Report

## Project

Webhook Validator DevSecOps Project

## Purpose

This document summarizes the security validation process for the Webhook Validator microservice.

The goal is to demonstrate a practical DevSecOps workflow where a simple Python API is tested, containerized, scanned, and documented using repeatable security practices.

---

## Security Model

The application receives webhook requests and validates their authenticity using HMAC SHA-256 signatures.

Basic flow:

```text
External sender
   ↓
Payload + X-Webhook-Signature
   ↓
FastAPI service
   ↓
HMAC SHA-256 verification
   ↓
Accept or reject request
