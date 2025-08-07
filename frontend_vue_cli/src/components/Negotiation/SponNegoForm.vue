<template>
    <h1>Negotiation Request</h1>
    <form  method="POST" class="form">
        <div class="form-group">
            <label for="message" class="form-label">Message:</label>
            <textarea id="message" name="message" class="form-control textarea-field" required></textarea>
        </div>
        <div class="form-group">
            <label for="sponsor_negotiation_payment_amt" class="form-label">Sponsor Negotiation Payment Amount:</label>
            <input type="number" id="sponsor_negotiation_payment_amt" name="sponsor_negotiation_payment_amt" class="form-control input-field" required>
        </div>
        <div class="form-group">
            <button type="submit" class="btn-submit">Create Request</button>
        </div>
    </form>
  </template>
  
  <script>
  export default {
    name: 'SponNegoForm'
  }
  </script>
  
  <style>
        .form {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 50px auto;
            max-width: 60%;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 15px;
            width: 100%;
        }

        .form-label {
            margin-bottom: 5px;
            font-weight: bold;
        }

        .input-field, .textarea-field {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #ccc;
            border-radius: 4px;
        }

        .textarea-field {
            height: 100px;
        }

        .btn-submit {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        .btn-submit:hover {
            background-color: #45a049;
        }
    </style>
  