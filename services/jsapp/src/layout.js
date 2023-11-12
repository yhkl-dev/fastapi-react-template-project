import React from "react";
import { Layout, theme } from "antd";
import { useState } from "react";
import "./App.css";
import DefaultLayoutHeader from "./components/DefaultLayoutHeader";
import DefaultLayoutSider from "./components/DefaultLayoutSider";
import DefaultLayoutFooter from "./components/DefaultLayoutFooter";
import DefaultLayoutContent from "./components/DefaultLayoutContent";

function DefaultLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  return (
    <Layout style={{ height: "100vh" }}>
      <DefaultLayoutSider collapsed={collapsed} />
      <Layout>
        <DefaultLayoutHeader
          collapsed={collapsed}
          setCollapsed={setCollapsed}
          colorBgContainer={colorBgContainer}
        />
        <DefaultLayoutContent />
        <DefaultLayoutFooter />
      </Layout>
    </Layout>
  );
}

export default DefaultLayout;
