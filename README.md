# Repo Table

**Repo Table** helps developers visualize all their GitHub repositories in a single, easy-to-read table. It exports your repository metadata (including name, owner, language, stars, license, and more) to a CSV file, making it simple to analyze or share your projects.

## Features

- **OAuth Device Flow** authentication for secure access to your private and public repositories.
- Fetches all repositories (handles pagination automatically).
- Exports repository details to a CSV file.
- Includes metadata such as owner, name, language, stars, license, type, archived status, template status, mirror status, and fork status.

## Usage

1. **Install dependencies**  
   Make sure you have Python 3.10+ and [uv](https://github.com/astral-sh/uv) installed.

   ```sh
   uv sync
   ```

2. **Run the exporter**

   ```sh
   uv run main.py
   ```

   By default, this will create a [`repos.csv`](repos.csv) file in your current directory.

   - To specify a different output file:

     ```sh
     uv run main.py --output my_repos.csv
     ```

3. **Authenticate**  
   The script will prompt you to authenticate via GitHub's Device Flow. Follow the instructions in your terminal to authorize access.

4. **View your table**  
   Open the generated CSV file with your favorite spreadsheet tool or data viewer.

## Example Output

| owner              | name                    | primary_language | stars | license | type   | archived | is_template | is_mirror | is_fork |
| ------------------ | ----------------------- | ---------------- | ----- | ------- | ------ | -------- | ----------- | --------- | ------- |
| riccardotornesello | hello-world-http-server | Python           | 0     | MIT     | Public | False    | False       | False     | False   |

## Contributing

Contributions are welcome! To get started:

1. **Fork the repository** and clone it locally.
2. **Create a new branch** for your feature or bugfix.
3. **Make your changes** and add tests if applicable.
4. **Submit a pull request** with a clear description of your changes.

Please ensure your code follows Python best practices and is well-documented.

---

**License:** See the [LICENSE](LICENSE) file for details.
**Maintainer:** [riccardotornesello](https://github.com/riccardotornesello)
