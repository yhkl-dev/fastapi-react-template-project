import React, { useMemo, useRef, useState } from "react";
import debounce from "lodash/debounce";
import { Select, Spin } from "antd";

function DebounceSelect({ fetchOptions, debounceTimeout = 800, ...props }) {
  const [fetching, setFetching] = useState(false);
  const [options, setOptions] = useState([]);
  const fetchRef = useRef(0);
  console.log(props);
  console.log(options);
  const debounceFetcher = useMemo(() => {
    const loadOptions = (value) => {
      fetchRef.current += 1;
      const fetchId = fetchRef.current;
      setFetching(true);
      fetchOptions(value).then((response) => {
        const results = [];
        console.log(response.data.data);
        if (response.data.data.sites) {
          response.data.data.sites.map((column) =>
            results.push({
              value: column.site_code,
              label: column.site_name,
            })
          );
          console.log(">>>>", results);
          if (fetchId !== fetchRef.current) {
            // for fetch callback order
            console.log("others-----------------------------------------");
            return;
          }
          setOptions(results);
          setFetching(false);
        }
      });
    };
    return debounce(loadOptions, debounceTimeout);
  }, [fetchOptions, debounceTimeout]);

  return (
    <Select
      allowClear
      showSearch
      labelInValue
      filterOption={false}
      onSearch={debounceFetcher}
      notFoundContent={fetching ? <Spin size="small" /> : null}
      {...props}
      options={options}
    />
  );
}

export default DebounceSelect;
