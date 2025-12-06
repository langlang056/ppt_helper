#!/bin/bash
# PPT Helper 服务管理脚本

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_status() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  PPT Helper 服务状态${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    
    echo -e "${YELLOW}后端服务:${NC}"
    systemctl status ppt-helper-backend --no-pager | head -n 3
    echo ""
    
    echo -e "${YELLOW}前端服务:${NC}"
    systemctl status ppt-helper-frontend --no-pager | head -n 3
    echo ""
    
    echo -e "${YELLOW}Nginx:${NC}"
    systemctl status nginx --no-pager | head -n 3
    echo ""
}

start_services() {
    echo -e "${GREEN}启动所有服务...${NC}\n"
    systemctl start ppt-helper-backend
    systemctl start ppt-helper-frontend
    systemctl start nginx
    echo -e "${GREEN}✓ 所有服务已启动${NC}\n"
    show_status
}

stop_services() {
    echo -e "${YELLOW}停止所有服务...${NC}\n"
    systemctl stop ppt-helper-backend
    systemctl stop ppt-helper-frontend
    echo -e "${GREEN}✓ 所有服务已停止${NC}\n"
    show_status
}

restart_services() {
    echo -e "${YELLOW}重启所有服务...${NC}\n"
    systemctl restart ppt-helper-backend
    systemctl restart ppt-helper-frontend
    systemctl restart nginx
    echo -e "${GREEN}✓ 所有服务已重启${NC}\n"
    show_status
}

show_logs() {
    echo -e "${BLUE}选择要查看的日志:${NC}"
    echo "1) 后端日志"
    echo "2) 前端日志"
    echo "3) Nginx 访问日志"
    echo "4) Nginx 错误日志"
    read -p "请选择 [1-4]: " choice
    
    case $choice in
        1)
            echo -e "${GREEN}查看后端日志 (Ctrl+C 退出)${NC}"
            journalctl -u ppt-helper-backend -f
            ;;
        2)
            echo -e "${GREEN}查看前端日志 (Ctrl+C 退出)${NC}"
            journalctl -u ppt-helper-frontend -f
            ;;
        3)
            echo -e "${GREEN}查看 Nginx 访问日志 (Ctrl+C 退出)${NC}"
            tail -f /var/log/nginx/access.log
            ;;
        4)
            echo -e "${GREEN}查看 Nginx 错误日志 (Ctrl+C 退出)${NC}"
            tail -f /var/log/nginx/error.log
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            ;;
    esac
}

update_code() {
    echo -e "${YELLOW}更新代码...${NC}\n"
    
    read -p "请输入项目路径 (例: /root/Documents/ppt_helper): " PROJECT_PATH
    
    if [ ! -d "$PROJECT_PATH" ]; then
        echo -e "${RED}错误: 项目目录不存在${NC}"
        exit 1
    fi
    
    cd "$PROJECT_PATH"
    
    # 拉取代码
    echo -e "${YELLOW}拉取最新代码...${NC}"
    git pull
    
    # 更新前端
    echo -e "${YELLOW}更新前端...${NC}"
    cd frontend
    npm install
    npm run build
    
    # 重启服务
    echo -e "${YELLOW}重启服务...${NC}"
    systemctl restart ppt-helper-backend
    systemctl restart ppt-helper-frontend
    
    echo -e "${GREEN}✓ 更新完成${NC}\n"
    show_status
}

# 检查是否为 root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}请使用 sudo 运行此脚本${NC}"
   exit 1
fi

# 主菜单
while true; do
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}  PPT Helper 服务管理${NC}"
    echo -e "${BLUE}========================================${NC}\n"
    echo "1) 查看服务状态"
    echo "2) 启动所有服务"
    echo "3) 停止所有服务"
    echo "4) 重启所有服务"
    echo "5) 查看日志"
    echo "6) 更新代码"
    echo "0) 退出"
    echo ""
    read -p "请选择操作 [0-6]: " choice
    
    case $choice in
        1)
            show_status
            ;;
        2)
            start_services
            ;;
        3)
            stop_services
            ;;
        4)
            restart_services
            ;;
        5)
            show_logs
            ;;
        6)
            update_code
            ;;
        0)
            echo -e "${GREEN}再见!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选择，请重试${NC}"
            ;;
    esac
done
