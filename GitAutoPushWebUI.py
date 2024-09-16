import gradio as gr
import argparse
from src.git_auto_push import git_auto_push
from src.log import get_logger
import os

logger = get_logger(__name__)

# 文件名用于存储路径
PATH_FILE = "git_repo_path.txt"

def read_git_repo_path():
    """从文件中读取 git_repo_path """
    if os.path.exists(PATH_FILE):
        with open(PATH_FILE, 'r') as file:
            return file.read().strip()
    else:
        return "/path/to/your/repo:branch"

def write_git_repo_path(path):
    """将 git_repo_path 写入文件 """
    with open(PATH_FILE, 'w') as file:
        file.write(path)
        logger.info(f"Write git_repo_path to {PATH_FILE}: {path}")
    return path
        

# 初始化状态变量
initial_git_repo_path = read_git_repo_path()


def main():
    # Define the interface
    with gr.Blocks() as demo:
        git_repo_path_state = gr.State(initial_git_repo_path)  # Store the git_repo_path

        with gr.TabItem("GitAutoPush"):
            gr.Markdown("## GitAutoPush")
            with gr.Row():
                git_repo_path = gr.Textbox(
                    label="Git Repo Path",
                    value=initial_git_repo_path,
                    lines=1,
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

    # Launch the interface
    parser = argparse.ArgumentParser(description="Demo")
    parser.add_argument(
        "--server_name", type=str, default="localhost", help="server name"
    )
    parser.add_argument("--server_port", type=int, default=8080, help="server port")
    parser.add_argument("--root_path", type=str, default=None, help="root path")
    args = parser.parse_args()

    demo.launch(
        server_name=args.server_name,
        server_port=args.server_port,
        root_path=args.root_path,
        show_api=False,
    )


if __name__ == "__main__":
    main()