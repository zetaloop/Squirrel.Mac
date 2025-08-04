# <small>`Squirrel.Mac` _but without signature verification_</small>

The Electron updater component for macOS, with signature verification removed.<br>
So that you can auto update your app without having to pAy aPpLe.

You should not use this in production.

<img width="200" src="https://github.com/user-attachments/assets/fc3ed443-04ad-480d-8ba8-9636167077a3"/>

## Just give me the binaries

[`--> Releases <--`](https://github.com/zetaloop/Squirrel.Mac/releases)

## Build my own

Checkout [Electron's build docs](https://www.electronjs.org/docs/latest/development/build-instructions-gn).

- Set up your build environment
  - Xcode, Python, Node.js, [**depot_tools**](https://www.electronjs.org/docs/latest/development/build-instructions-gn#gn-prerequisites), etc.
  - a day of free time

- Get the Electron code
    ```bash
    mkdir electron && cd electron
    gclient config --name "src/electron" --unmanaged https://github.com/electron/electron
    gclient sync --with_branch_heads --with_tags
    # ↑ This can take hours and use up to 100GB of disk space.

    cd src
    export CHROMIUM_BUILDTOOLS_PATH=`pwd`/buildtools
    ```

- Apply this patch to remove the signature verification logic
    ```bash
    cd third_party/squirrel.mac
    curl https://raw.githubusercontent.com/zetaloop/Squirrel.Mac/refs/heads/mod/refactor_remove_signature_verification_logic.patch | git am
    cd ../..
    ```

- Generate build configs
    ```bash
    gn gen out/Release-arm64 --args="import(\"//electron/build/args/testing.gn\") target_cpu=\"arm64\""
    gn gen out/Release-x64 --args="import(\"//electron/build/args/testing.gn\") target_cpu=\"x64\""
    ```

- Build
    ```bash
    # arm64
    ninja -C out/Release-arm64 squirrel_framework
    rm out/Release-arm64/Squirrel.framework/Headers
    rm -r out/Release-arm64/Squirrel.framework/Versions/A/Headers

    # x64
    ninja -C out/Release-x64 squirrel_framework
    rm out/Release-x64/Squirrel.framework/Headers
    rm -r out/Release-x64/Squirrel.framework/Versions/A/Headers

    # Universal
    ditto out/Release-arm64/Squirrel.framework out/Release-universal/Squirrel.framework
    lipo -create out/Release-arm64/Squirrel.framework/Squirrel out/Release-x64/Squirrel.framework/Squirrel -output out/Release-universal/Squirrel.framework/Versions/A/Squirrel
    lipo -create out/Release-arm64/Squirrel.framework/Resources/ShipIt out/Release-x64/Squirrel.framework/Resources/ShipIt -output out/Release-universal/Squirrel.framework/Versions/A/Resources/ShipIt
    ```

- Package
    ```bash
    ditto -c -k -X --norsrc --noqtn --keepParent out/Release-arm64/Squirrel.framework out/Squirrel-arm64.zip
    ditto -c -k -X --norsrc --noqtn --keepParent out/Release-x64/Squirrel.framework out/Squirrel-x64.zip
    ditto -c -k -X --norsrc --noqtn --keepParent out/Release-universal/Squirrel.framework out/Squirrel-universal.zip
    ```
- You'll find these in the `electron/src/out` directory:

  `Squirrel-arm64.zip`<br>
  `Squirrel-x64.zip`<br>
  `Squirrel-universal.zip`
