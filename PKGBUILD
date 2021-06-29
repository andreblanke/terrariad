# Maintainer: Andre Blanke

pkgname='terrariad'
pkgver='1.0.0'
pkgrel=1
pkgdesc='Terraria server daemon providing socket activation'
arch=('any')
url='https://github.com/andreblanke/terrariad'
license=('MIT')
depends=('python')
source=("https://github.com/andreblanke/$pkgname/archive/refs/tags/v$pkgver.zip")
sha256sums=('1ff491f5dcf62a6931202a3375713a07798547c6d1dd5d6a2453ec8c01a586e1')

package() {
    cd "$pkgname-$pkgver"

    install -D --mode=755 'terrariad.py'      "$pkgdir/usr/bin/terrariad"
    install -D --mode=644 'terrariad.service' "$pkgdir/usr/lib/systemd/system/terrariad.service"
    install -D --mode=644 'LICENSE.txt'       "$pkgdir/usr/share/licenses/terrariad/LICENSE.txt"
}
