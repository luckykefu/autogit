import os
import gradio as gr
from .git_auto_push import git_auto_push
from .log import get_logger

logger = get_logger(__file__)
output_dir =  "output"

PATH_FILE = os.path.join(output_dir, "git_repo_path.txt")


def read_git_repo_path():
    """从文件中读取 git_repo_path"""
    if os.path.exists(PATH_FILE):
        with open(PATH_FILE, "r") as file:
            return file.read().strip()
    else:
        return "/path/to/your/repo branch"


def write_git_repo_path(path):
    """将 git_repo_path 写入文件"""
    with open(PATH_FILE, "w") as file:
        file.write(path)
        logger.info(f"Write git_repo_path to {PATH_FILE}: {path}")
    return path


# 初始化状态变量
initial_git_repo_path = read_git_repo_path()


def demo_gitautopush():
    with gr.Blocks() as gitautopushdemo:
        git_repo_path_state = gr.State(initial_git_repo_path)  # Store the git_repo_path

        gr.Markdown("## GitAutoPush")
        with gr.Row():
            git_repo_path = gr.Textbox(
                label="Git Repo Path",
                value=initial_git_repo_path,
                lines=5,
            )
            git_repo_path.change(
                fn=lambda x: write_git_repo_path(x),  # 更新文件中的路径
                inputs=[git_repo_path],
                outputs=[git_repo_path],
            )  # 更新 State

            git_message = gr.Textbox(label="Git Message", value="", lines=2)
        with gr.Row():
            git_username = gr.Textbox(label="Git Username", value="")
            git_email = gr.Textbox(label="Git Email", value="")
        with gr.Row():
            git_auto_push_btn = gr.Button("GitAutoPush")

            git_auto_push_btn.click(
                fn=git_auto_push,
                inputs=[
                    git_repo_path_state,  # 使用 State 而不是 Textbox
                    git_message,
                    git_username,
                    git_email,
                ],
                outputs=[],
            )
    return gitautopushdemo
