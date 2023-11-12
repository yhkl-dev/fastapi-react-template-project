import React from "react";
import { Layout, Menu } from "antd";
import { Link } from "react-router-dom";
import { FileOutlined } from "@ant-design/icons";

const { Sider } = Layout;

function DefaultLayoutSider({ collapsed }) {
  const menuItems = [
    {
      key: "1",
      icon: <FileOutlined />,
      children: <Link to="/">Service Account</Link>,
      label: "Service Account",
    },
  ];

  return (
    <Sider collapsible collapsed={collapsed} trigger={null}>
      <div className="demo-logo-vertical" />
      <Menu theme="dark" mode="vertical" defaultSelectedKeys={["1"]}>
        {menuItems.map((item) => (
          <Menu.Item key={item.key} icon={item.icon}>
            {item.children}
          </Menu.Item>
        ))}
      </Menu>
    </Sider>
  );
}

export default DefaultLayoutSider;
