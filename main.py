import random
import time

# --- Simulate an external service or complex operation ---
def _simulate_data_processing_service(data):
    """
    Simulates a data processing service that can:
    1. Fail due to invalid data content (e.g., business rule violation).
    2. Fail randomly due to transient issues (e.g., network, server errors).
    """
    # --- Robustness: Service-level content validation ---
    # This ensures the service itself can validate business rules.
    if data["value"] < 0:
        raise ValueError("Data content error: 'value' cannot be negative for processing.")

    # Simulate random transient failures (e.g., network issues, temporary server overload)
    if random.random() < 0.4:  # 40% chance of transient failure
        if random.random() < 0.5:
            raise ConnectionError("Simulated network connection error.")
        else:
            raise RuntimeError("Simulated service internal error.")

    # Simulate successful processing
    processed_value = data["value"] * 2
    return {"original": data["value"], "processed": processed_value, "status": "success"}

# --- Main function demonstrating Robustness and Reliability ---
def process_data_with_resilience(input_data, max_retries=3, retry_delay_seconds=1):
    """
    Processes input data, demonstrating robustness through input validation
    and error handling, and reliability through retries and a fallback mechanism.
    """
    print(f"\nAttempting to process data: {input_data}")

    # --- Robustness: Initial Input Format Validation ---
    # Ensures the system can handle unexpected or malformed input gracefully
    # before even attempting to call the service.
    if not isinstance(input_data, dict) or "value" not in input_data or not isinstance(input_data["value"], (int, float)):
        print(f"  ERROR: Invalid input data format. Expected a dict with a numeric 'value' key. (Robustness)")
        return {"status": "failed", "reason": "Invalid input format"}

    attempts = 0
    while attempts <= max_retries:
        try:
            print(f"  Attempt {attempts + 1}/{max_retries + 1}...")
            # --- Robustness: Error Handling ---
            # Catches expected exceptions from the service call.
            result = _simulate_data_processing_service(input_data)
            print(f"  SUCCESS: Data processed. Result: {result} (Robustness)")
            return result
        except (ConnectionError, RuntimeError) as e:
            # --- Reliability: Retry Mechanism ---
            # If a transient error occurs, the system attempts to recover by retrying.
            print(f"  WARNING: Transient error encountered: {e}. Retrying in {retry_delay_seconds}s... (Reliability)")
            attempts += 1
            if attempts <= max_retries:
                time.sleep(retry_delay_seconds)
            else:
                print(f"  All {max_retries + 1} attempts failed due to transient errors. (Reliability)")
                break
        except ValueError as e:
            # --- Robustness: Specific Error Handling for Bad Data Content ---
            # Catches errors related to the data content itself, not transient issues.
            # No retry here as the data itself is problematic.
            print(f"  ERROR: Data content error: {e}. Cannot retry with same bad data. (Robustness)")
            return {"status": "failed", "reason": f"Data content error: {e}"}
        except Exception as e:
            # --- Robustness: Generic Error Handling ---
            # Catches any other unexpected errors, ensuring the application doesn't crash.
            print(f"  CRITICAL ERROR: An unexpected error occurred: {e}. (Robustness)")
            return {"status": "failed", "reason": f"Unexpected error: {e}"}

    # --- Reliability: Fallback Mechanism ---
    # If all retries fail, provide a graceful fallback or a clear failure message,
    # ensuring the system continues to operate predictably.
    print(f"  FAILURE: Could not process data after {max_retries + 1} attempts. Providing fallback. (Reliability)")
    return {"status": "failed", "reason": "Service unavailable after multiple retries", "fallback_action": "notify_admin"}

# --- Example Usage ---
if __name__ == "__main__":
    print("--- Demonstrating Robustness and Reliability in System Operations ---")

    # Scenario 1: Successful processing
    process_data_with_resilience({"value": 10})

    # Scenario 2: Transient failures, eventually succeeds (Reliability)
    # Run multiple times to observe different outcomes due to randomness.
    process_data_with_resilience({"value": 20})

    # Scenario 3: All retries fail (Reliability with Fallback)
    # This scenario might occur if the simulated service consistently fails.
    process_data_with_resilience({"value": 30})

    # Scenario 4: Invalid input format (Robustness - Initial Input Validation)
    process_data_with_resilience("not a dict")
    process_data_with_resilience({"key": "value"}) # Missing 'value' key
    process_data_with_resilience({"value": "text"}) # Non-numeric value

    # Scenario 5: Service-specific data content error (Robustness - Service-level Content Validation)
    process_data_with_resilience({"value": -5})
