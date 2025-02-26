<h1 align="center">Git Scheduler</h1>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"/>
  <img src="https://img.shields.io/badge/Git--Scheduler-1.1.0-yellowgreen.svg" alt="Git Scheduler Version" />
  <img src="https://img.shields.io/badge/schedule-1.2.2-green.svg" alt="Schedule Version">
</p>

<p align="center">Git Scheduler is a Python tool that allows you to schedule Git commits and pushes at a specific time.</p>

<h2>Features</h2>

<ol>
  <li>Schedule commits for a specific time.</li>
  <li>Automatically push changes to your Git repository.</li>
  <li>Track commit history with timestamp and commit details.</li>
  <li>Easy-to-use command-line interface with prompts.</li>
  <li>View your commit history with timestamps and commit messages when you rerun the tool.</li>
  <li>Option to select multiple files to commit if there are changes in the repository.</li>
</ol>

<h2>Installation</h2>

<ol>
  <li>
    <p>Clone the repository:</p>
    <pre><code>git clone https://github.com/anonymByte-404/git-scheduler.git</code></pre>
  </li>
  <li>
    <p>Install dependencies:</p>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ol>

<h2>Usage</h2>

<p>Run the program:</h2>

<pre><code>python src/main.py</code></pre>

<p>Follow the prompts to schedule your commit, choose changes to commit, and review your commit history. The tool will allow you to commit at the scheduled time and push changes to your repository automatically.</p> 

<h2>Commit History</h2> 

<p>Your commit history is automatically saved in the <code>data/commit_history.json</code> file. This history includes:</p> 

<ul> 
  <li>Repository path</li> 
  <li>Branch name</li> 
  <li>Commit message</li> 
  <li>Scheduled commit time</li> 
  <li>Timestamp of scheduling</li> 
</ul>

<p>You can view your commit history in real-time when you run the program again. This feature allows you to keep track of all scheduled commits.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>