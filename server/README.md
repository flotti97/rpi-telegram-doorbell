## Setting up a Python Virtual Environment

1. Open a terminal and navigate to this directory:

   ```
   cd server/notifier
   ```

2. Create a virtual environment (replace `.venv` with your preferred name):

   ```
   python -m venv .venv
   ```

3. Activate the virtual environment:

   - On **Windows**:
     ```
     .venv\Scripts\activate
     ```
   - On **Linux/macOS**:
     ```
     source .venv/bin/activate
     ```

4. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

5. Run the notifier script as needed.